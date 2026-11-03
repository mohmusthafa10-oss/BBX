#!/usr/bin/env python3
"""evaluate.py: scores extracted fields against the synthetic ground truth, for raw OCR and preprocessed OCR.

Usage: python3 evaluate.py --samples samples --out out
"""
import argparse
import json
from pathlib import Path

from invoice_extractor import parse_date

FIELDS = ["invoice_no", "date", "vendor", "subtotal", "tax", "total", "items"]


def norm_text(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())


def score(fields, gt):
    d = parse_date(fields.get("date") or "")
    expected_total = gt["total_printed"]
    items = [i for i in fields.get("items") or [] if i.get("amount") is not None]
    got_amounts = sorted(round(i["amount"], 2) for i in items)
    exp_amounts = sorted(round(a, 2) for _, _, a in gt["items"])
    checks = {
        "invoice_no": norm_text(fields.get("invoice_no")) == norm_text(gt["invoice_no"]),
        "date": d is not None and d.isoformat() == gt["date"],
        "vendor": norm_text(fields.get("vendor")) == norm_text(gt["vendor"]),
        "subtotal": fields.get("subtotal") is not None and abs(fields["subtotal"] - gt["subtotal"]) < 0.005,
        "tax": fields.get("tax") is not None and abs(fields["tax"] - gt["tax"]) < 0.005,
        "total": fields.get("total") is not None and abs(fields["total"] - expected_total) < 0.005,
        "items": got_amounts == exp_amounts,
    }
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", default="samples")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    gt = {g["file"].rsplit(".", 1)[0]: g for g in json.loads((Path(args.samples) / "ground_truth.json").read_text())}
    out = Path(args.out)
    lines = ["| document | " + " | ".join(f"{f} raw/pre" for f in FIELDS) + " |",
             "|---|" + "---|" * len(FIELDS)]
    totals = {"raw": 0, "pre": 0}
    n_fields = 0
    for name, g in gt.items():
        raw = score(json.loads((out / "fields" / f"{name}.raw.json").read_text()), g)
        pre = score(json.loads((out / "fields" / f"{name}.pre.json").read_text()), g)
        totals["raw"] += sum(raw.values())
        totals["pre"] += sum(pre.values())
        n_fields += len(FIELDS)
        cells = []
        for k in FIELDS:
            cells.append(f"{'Y' if raw[k] else 'N'}/{'Y' if pre[k] else 'N'}")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append(f"Fields correct, raw OCR: {totals['raw']}/{n_fields}. "
                 f"Fields correct, preprocessed OCR: {totals['pre']}/{n_fields}.")
    (out / "evaluation.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
