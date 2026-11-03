#!/usr/bin/env python3
"""invoice_extractor.py: text-layer detection, preprocessing, OCR with and without preprocessing,
two-way field extraction (regex and word positions), validation, and routing to accepted/ or needs_review/.

Usage: python3 invoice_extractor.py samples --out out
"""
import argparse
import csv
import json
import logging
import re
import shutil
from datetime import date, datetime
from pathlib import Path

import cv2
import numpy as np
import pdfplumber
import pytesseract
from pytesseract import Output

CONF_THRESHOLD = 80.0   # mean word confidence below this routes to needs_review/
MIN_TEXT_CHARS = 40     # fewer non-space characters than this => no usable text layer
OCR_CFG = "--oem 3 --psm 6"
MONEY = r"[\d,]+\.\d{2}"
DATE = r"\b(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2} [A-Za-z]{3,9} \d{4}|[A-Za-z]{3,9} \d{1,2}, \d{4})\b"
DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"]
log = logging.getLogger("invoice")


# ---------- loading and text-layer detection ----------

def load_pages(path: Path):
    """Return page images in BGR. PDFs are rasterised at 300 dpi; only page 1 is used (invoices are one page)."""
    if path.suffix.lower() == ".pdf":
        with pdfplumber.open(path) as pdf:
            pil = pdf.pages[0].to_image(resolution=300).original.convert("RGB")
        return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    return cv2.imread(str(path))


def text_layer(path: Path):
    """Return (text, words) from the PDF text layer, or ("", []) for image files."""
    if path.suffix.lower() != ".pdf":
        return "", []
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
        words = [{"text": w["text"], "conf": None, "left": w["x0"], "top": w["top"],
                  "line": round(w["top"] / 4)} for w in page.extract_words()]
    return text, words


# ---------- preprocessing: each step saves its intermediate image ----------

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img


def adaptive_threshold(gray):
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)


def deskew(binary, max_deg=10.0):
    """Rotate by the angle that makes text rows most distinct (largest variance of row ink counts)."""
    ink = (binary < 128).astype(np.float32)
    small = cv2.resize(ink, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    h, w = small.shape
    best_angle, best_score = 0.0, -1.0
    for angle in np.arange(-max_deg, max_deg + 0.01, 0.25):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), float(angle), 1.0)
        rotated = cv2.warpAffine(small, M, (w, h))
        score = float(np.var(rotated.sum(axis=1)))
        if score > best_score:
            best_angle, best_score = float(angle), score
    H, W = binary.shape
    M = cv2.getRotationMatrix2D((W / 2, H / 2), best_angle, 1.0)
    return cv2.warpAffine(binary, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=255), best_angle


def denoise(binary):
    return cv2.medianBlur(binary, 3)


def preprocess(img, name: str, inter_dir: Path):
    step_dir = inter_dir / name
    step_dir.mkdir(parents=True, exist_ok=True)
    gray = grayscale(img)
    cv2.imwrite(str(step_dir / "1_gray.png"), gray)
    binary = adaptive_threshold(gray)
    cv2.imwrite(str(step_dir / "2_threshold.png"), binary)
    straight, angle = deskew(binary)
    cv2.imwrite(str(step_dir / "3_deskew.png"), straight)
    clean = denoise(straight)
    cv2.imwrite(str(step_dir / "4_denoise.png"), clean)
    log.info("%s: preprocessing done, deskew angle %.2f deg", name, angle)
    return clean, angle


# ---------- OCR with per-word confidence ----------

def ocr(img):
    data = pytesseract.image_to_data(img, config=OCR_CFG, output_type=Output.DICT)
    words = []
    for i, text in enumerate(data["text"]):
        conf = float(data["conf"][i])
        if text.strip() and conf >= 0:
            words.append({"text": text.strip(), "conf": conf, "left": data["left"][i], "top": data["top"][i],
                          "line": (data["block_num"][i], data["par_num"][i], data["line_num"][i])})
    text = pytesseract.image_to_string(img, config=OCR_CFG)
    mean_conf = float(np.mean([w["conf"] for w in words])) if words else 0.0
    return {"text": text, "words": words, "mean_conf": mean_conf,
            "chars": sum(not c.isspace() for c in text)}


# ---------- position helpers ----------

def lines_of(words):
    groups = {}
    for w in words:
        groups.setdefault(w["line"], []).append(w)
    lines = [sorted(g, key=lambda w: w["left"]) for g in groups.values()]
    return sorted(lines, key=lambda g: min(w["top"] for w in g))


def rest_of_line(words, anchor, pattern):
    """Find the anchor word on a line and return the first pattern match to its right."""
    for line in lines_of(words):
        for i, w in enumerate(line):
            if w["text"].rstrip(":").lower() == anchor.lower():
                m = re.search(pattern, " ".join(x["text"] for x in line[i + 1:]))
                if m:
                    return m.group(0)
    return None


def items_by_position(words):
    lines = lines_of(words)
    header = next((ln for ln in lines if {"Description", "Amount"} <= {w["text"] for w in ln}), None)
    if header is None:
        return []
    cols = {w["text"]: w["left"] for w in header}
    qty_x = cols.get("Qty", cols["Amount"] - 400)
    amount_x = cols["Amount"]
    # Column tolerance comes from the header spacing, so it works at any image or PDF scale.
    unit_x = cols.get("Unit", amount_x - 400)
    tolerance = max((amount_x - unit_x) / 2, 1)
    items = []
    for line in lines[lines.index(header) + 1:]:
        texts = [w["text"].rstrip(":") for w in line]
        if any(t in ("Subtotal", "Tax", "Total") for t in texts):
            break
        money = [w for w in line if re.fullmatch(MONEY, w["text"])]
        desc_tokens = [w["text"] for w in line if w["left"] < qty_x - 30]
        if not desc_tokens and not money:
            continue
        # The amount is the number in the Amount column, not the rightmost number on the row.
        in_column = [w for w in money if abs(w["left"] - amount_x) < tolerance]
        nearest = min(in_column, key=lambda w: abs(w["left"] - amount_x)) if in_column else None
        amount = float(nearest["text"].replace(",", "")) if nearest else None
        qty = [w["text"] for w in line if w["text"].isdigit() and qty_x - 30 <= w["left"] < amount_x - 100]
        items.append({"description": " ".join(desc_tokens), "qty": int(qty[0]) if qty else None, "amount": amount})
    return items


def vendor_by_position(words):
    lines = lines_of(words)
    if not lines:
        return None
    top = lines[0]
    invoice_tok = next((w for w in top if w["text"].upper() == "INVOICE"), None)
    kept = [w["text"] for w in top if invoice_tok is None or w["left"] < invoice_tok["left"]]
    return re.sub(r"^[^A-Za-z0-9]+", "", " ".join(kept)).strip() or None


# ---------- regex extraction on the OCR / text-layer string ----------

def fields_by_regex(text):
    def first(pattern, flags=0):
        m = re.search(pattern, text, flags)
        return m.group(1).strip() if m else None

    money_to_float = lambda s: float(s.replace(",", "")) if s else None
    first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), None)
    items = []
    for ln in text.splitlines():
        m = re.match(rf"^\s*(?P<desc>.+?)\s+(?P<qty>\d+)\s+(?P<unit>{MONEY})\s+(?P<amount>{MONEY})\s*$", ln)
        if m:
            items.append({"description": m["desc"].strip(), "qty": int(m["qty"]),
                          "amount": float(m["amount"].replace(",", ""))})
    return {
        "invoice_no": first(r"Invoice\s*No\.?\s*:?\s*([A-Z0-9][A-Z0-9-]*)", re.IGNORECASE),
        "date": first(DATE, re.IGNORECASE),
        "vendor": re.sub(r"^[^A-Za-z0-9]+", "", re.sub(r"\s*INVOICE$", "", first_line or "")).strip() or None,
        "subtotal": money_to_float(first(rf"Subtotal\s*:?\s*\$?\s*({MONEY})", re.IGNORECASE)),
        "tax": money_to_float(first(rf"Tax\b[^\n]*?({MONEY})", re.IGNORECASE)),
        "total": money_to_float(first(rf"^\s*Total\s*:?\s*\$?\s*({MONEY})", re.MULTILINE)),
        "items": items,
    }


def fields_by_position(words):
    money = lambda s: float(s.replace(",", "")) if s else None
    return {
        "invoice_no": rest_of_line(words, "No", r"[A-Z0-9][A-Z0-9-]*\d[A-Z0-9-]*"),
        "date": rest_of_line(words, "Date", DATE),
        "vendor": vendor_by_position(words),
        "subtotal": money(rest_of_line(words, "Subtotal", MONEY)),
        "tax": money(rest_of_line(words, "Tax", MONEY)),
        "total": money(rest_of_line(words, "Total", MONEY)),
        "items": items_by_position(words),
    }


def merge(by_text, by_pos):
    """Prefer the regex value; use the positional value when regex found nothing. Record agreement."""
    out, sources, disagreements = {}, {}, []
    for key in ["invoice_no", "date", "vendor", "subtotal", "tax", "total", "items"]:
        t, p = by_text.get(key), by_pos.get(key)
        if key == "items":
            out[key] = t or p or []
            sources[key] = "regex" if t else ("position" if p else "none")
            if t and p and len(t) != len(p):
                disagreements.append(f"items: regex {len(t)} rows vs position {len(p)} rows")
            elif t and p and any(abs(a["amount"] - b["amount"]) > 0.005 for a, b in zip(t, p) if b["amount"] is not None):
                disagreements.append("items: amounts differ between regex and position")
            continue
        out[key] = t if t not in (None, "") else p
        sources[key] = "regex" if t not in (None, "") else ("position" if p not in (None, "") else "none")
        if t not in (None, "") and p not in (None, "") and str(t).lower() != str(p).lower():
            if not (isinstance(t, float) and isinstance(p, float) and abs(t - p) < 0.005):
                disagreements.append(f"{key}: regex {t!r} vs position {p!r}")
    return out, sources, disagreements


# ---------- validation ----------

def parse_date(s):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except (ValueError, TypeError):
            pass
    return None


def validate(f):
    fails = []
    for key in ["invoice_no", "date", "vendor", "subtotal", "tax", "total"]:
        if f.get(key) in (None, ""):
            fails.append(f"missing {key}")
    items = f.get("items") or []
    unreadable = [i["description"] or "(blank row)" for i in items if i["amount"] is None]
    if unreadable:
        fails.append(f"unreadable line amount on: {', '.join(unreadable)}")
    items = [i for i in items if i["amount"] is not None]
    if not items:
        fails.append("no line items found")
    elif f.get("subtotal") is not None:
        item_sum = round(sum(i["amount"] for i in items), 2)
        if abs(item_sum - f["subtotal"]) > 0.01:
            fails.append(f"line items sum {item_sum:.2f} != subtotal {f['subtotal']:.2f}")
    if None not in (f.get("subtotal"), f.get("tax"), f.get("total")):
        if abs(f["subtotal"] + f["tax"] - f["total"]) > 0.01:
            fails.append(f"subtotal + tax {f['subtotal'] + f['tax']:.2f} != total {f['total']:.2f}")
    if f.get("date"):
        d = parse_date(f["date"])
        if d is None:
            fails.append(f"unparseable date {f['date']!r}")
        elif not (date(2000, 1, 1) <= d <= date.today()):
            fails.append(f"implausible date {d.isoformat()}")
    return fails


# ---------- per-document pipeline ----------

def process(path: Path, out: Path):
    name = path.stem
    log.info("=== %s", path.name)
    text_str, pdf_words = text_layer(path)
    has_text_layer = len(re.sub(r"\s", "", text_str)) >= MIN_TEXT_CHARS
    path_used = "text_layer" if has_text_layer else "ocr"
    log.info("%s: text layer chars=%d -> path=%s", name, len(re.sub(r"\s", "", text_str)), path_used)

    img = load_pages(path)
    raw = ocr(img)                                  # OCR without preprocessing
    pre_img, angle = preprocess(img, name, out / "intermediate")
    pre = ocr(pre_img)                              # OCR with preprocessing
    log.info("%s: OCR raw conf=%.1f chars=%d | preprocessed conf=%.1f chars=%d",
             name, raw["mean_conf"], raw["chars"], pre["mean_conf"], pre["chars"])

    (out / "fields").mkdir(parents=True, exist_ok=True)
    for label, res in (("raw", raw), ("pre", pre)):
        fields_ocr, _, _ = merge(fields_by_regex(res["text"]), fields_by_position(res["words"]))
        (out / "fields" / f"{name}.{label}.json").write_text(json.dumps(fields_ocr, indent=2))
    (out / "ocr").mkdir(parents=True, exist_ok=True)
    (out / "ocr" / f"{name}.raw.txt").write_text(raw["text"])
    (out / "ocr" / f"{name}.pre.txt").write_text(pre["text"])

    if has_text_layer:
        body, words, chosen_conf = text_str, pdf_words, None
        (out / "ocr" / f"{name}.textlayer.txt").write_text(text_str)
        chosen_label = "text_layer"
    else:
        chosen = pre if pre["mean_conf"] >= raw["mean_conf"] else raw
        chosen_label = "preprocessed" if chosen is pre else "raw"
        body, words, chosen_conf = chosen["text"], chosen["words"], chosen["mean_conf"]
        log.info("%s: extraction uses %s OCR (higher mean confidence)", name, chosen_label)

    by_text = fields_by_regex(body)
    by_pos = fields_by_position(words)
    fields, sources, disagreements = merge(by_text, by_pos)
    fails = validate(fields)
    if disagreements:
        log.info("%s: regex vs position disagreements: %s", name, "; ".join(disagreements))

    reasons = list(fails)
    if disagreements:
        reasons.append("regex and position extraction disagree: " + "; ".join(disagreements))
    if not has_text_layer and chosen_conf < CONF_THRESHOLD:
        reasons.insert(0, f"mean OCR confidence {chosen_conf:.1f} below {CONF_THRESHOLD:.0f}")
    dest = "needs_review" if reasons else "accepted"
    (out / dest).mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, out / dest / path.name)
    if reasons:
        (out / dest / f"{name}.reasons.json").write_text(json.dumps(reasons, indent=2))
    log.info("%s: route=%s %s", name, dest, reasons if reasons else "")

    return {
        "document": path.name, "path": path_used, "ocr_used": chosen_label,
        "raw_chars": raw["chars"], "pre_chars": pre["chars"],
        "raw_conf": round(raw["mean_conf"], 1), "pre_conf": round(pre["mean_conf"], 1),
        "deskew_deg": round(angle, 2),
        "invoice_no": fields["invoice_no"], "date": fields["date"], "vendor": fields["vendor"],
        "subtotal": fields["subtotal"], "tax": fields["tax"], "total": fields["total"],
        "items": len(fields["items"]),
        "items_sum": round(sum(i["amount"] for i in fields["items"]), 2),
        "field_sources": "; ".join(f"{k}={v}" for k, v in sources.items()),
        "regex_position_disagreements": len(disagreements),
        "confidence": round(chosen_conf, 1) if chosen_conf is not None else "n/a (text layer)",
        "validation": "PASS" if not fails else "FAIL: " + "; ".join(fails),
        "route": dest,
        "route_reasons": "; ".join(reasons),
    }


def write_outputs(rows, out: Path):
    cols = list(rows[0].keys())
    with open(out / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(out / "results.md", "w") as f:
        f.write("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n")
        for r in rows:
            f.write("| " + " | ".join(str(r[c]) for c in cols) + " |\n")


def write_comparison(rows, out: Path):
    comp = []
    for r in rows:
        gain_chars = (r["pre_chars"] - r["raw_chars"]) / r["raw_chars"] * 100 if r["raw_chars"] else float("nan")
        comp.append({"document": r["document"], "raw_chars": r["raw_chars"], "pre_chars": r["pre_chars"],
                     "char_change_pct": round(gain_chars, 1), "raw_conf": r["raw_conf"],
                     "pre_conf": r["pre_conf"], "conf_gain": round(r["pre_conf"] - r["raw_conf"], 1)})
    with open(out / "comparison.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(comp[0].keys()))
        w.writeheader()
        w.writerows(comp)
    return comp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(out / "run.log", mode="w"), logging.StreamHandler()])
    files = sorted(p for p in Path(args.input_dir).iterdir() if p.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg"})
    rows = [process(p, out) for p in files]
    write_outputs(rows, out)
    comp = write_comparison(rows, out)
    log.info("wrote results.csv, results.md, comparison.csv to %s", out)
    print(json.dumps({"documents": len(rows),
                      "accepted": sum(r["route"] == "accepted" for r in rows),
                      "needs_review": sum(r["route"] == "needs_review" for r in rows),
                      "mean_conf_gain_ocr": round(float(np.mean([c["conf_gain"] for c in comp if c["raw_conf"] or c["pre_conf"]])), 1)}, indent=2))


if __name__ == "__main__":
    main()
