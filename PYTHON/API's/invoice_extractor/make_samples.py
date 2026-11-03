# make_samples.py: generates 8 synthetic invoices (clean scans, phone photos, low-res, digital PDF, scanned PDF) with ground truth.
import json
import random
from datetime import date, timedelta
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

W, H = 2480, 3508  # A4 at 300 dpi
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = Path("samples")
VENDORS = ["Northwind Office Supply Ltd", "Harbor Freight Services", "Bluebird Print & Design",
           "Cedar Point Logistics", "Maple & Oak Stationers", "Summit Software Pty"]
ITEMS = ["Printer paper A4 (case)", "Toner cartridge black", "Laptop stand", "Ergonomic chair",
         "USB-C cable 2m", "Whiteboard markers (box)", "Network switch 8-port", "Consulting hours"]
DATE_FORMATS = ["%d/%m/%Y", "%d %b %Y", "%b %d, %Y"]


def money(v):
    return f"{v:,.2f}"


def make_invoice(rng, error=False):
    items = []
    for desc in rng.sample(ITEMS, rng.randint(3, 5)):
        qty = rng.randint(1, 9)
        unit = round(rng.uniform(4, 480), 2)
        items.append({"description": desc, "qty": qty, "unit": unit, "amount": round(qty * unit, 2)})
    subtotal = round(sum(i["amount"] for i in items), 2)
    rate = rng.choice([5, 8, 10])
    tax = round(subtotal * rate / 100, 2)
    total = round(subtotal + tax, 2)
    d = date(2025, 1, 1) + timedelta(days=rng.randint(0, 600))
    fmt = rng.choice(DATE_FORMATS)
    return {
        "invoice_no": f"INV-{rng.randint(1000, 9999)}",
        "date": d.isoformat(),
        "date_display": d.strftime(fmt),
        "vendor": rng.choice(VENDORS),
        "items": items,
        "subtotal": subtotal,
        "tax_rate": rate,
        "tax": tax,
        "total": total,
        "printed_total": round(total + 10, 2) if error else total,  # deliberate arithmetic error
    }


def layout(inv, variant):
    """Returns (x, y_top, text, size_px, bold) lines. Shared by PIL images and reportlab PDFs."""
    L = []
    add = lambda x, y, t, s=44, b=False: L.append((x, y, t, s, b))
    add(150, 200, inv["vendor"], 70, True)
    add(150, 300, "12 Industrial Road, Sample City", 40)
    add(150, 350, "accounts@example.com", 40)
    add(1700, 200, "INVOICE", 90, True)
    add(1700, 330, f"Invoice No: {inv['invoice_no']}", 40)
    add(1700, 390, f"Date: {inv['date_display']}", 40)
    add(150, 600, "Bill to: Sample Customer Co", 44)
    add(150, 700, "Due on receipt", 40)
    cols = {"desc": 150, "qty": 1300, "unit": 1600, "amt": 2050} if variant == "A" else \
           {"desc": 150, "qty": 1150, "unit": 1500, "amt": 1900}
    add(cols["desc"], 1000, "Description", 44, True)
    add(cols["qty"], 1000, "Qty", 44, True)
    add(cols["unit"], 1000, "Unit price", 44, True)
    add(cols["amt"], 1000, "Amount", 44, True)
    y = 1100
    for it in inv["items"]:
        add(cols["desc"], y, it["description"], 44)
        add(cols["qty"], y, str(it["qty"]), 44)
        add(cols["unit"], y, money(it["unit"]), 44)
        add(cols["amt"], y, money(it["amount"]), 44)
        y += 110
    y += 120
    lab_x = cols["unit"] if variant == "A" else cols["qty"]
    add(lab_x, y, "Subtotal", 44)
    add(cols["amt"], y, money(inv["subtotal"]), 44)
    add(lab_x, y + 90, f"Tax ({inv['tax_rate']}%)", 44)
    add(cols["amt"], y + 90, money(inv["tax"]), 44)
    add(lab_x, y + 200, "Total", 50, True)
    add(cols["amt"], y + 200, money(inv["printed_total"]), 50, True)
    return L


def draw_pil(lines):
    img = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(img)
    for x, y, t, s, b in lines:
        d.text((x, y), t, font=ImageFont.truetype(FONT_B if b else FONT, s), fill=25)
    return np.array(img)


def clean_scan(img, rng):
    noisy = np.clip(img.astype(float) + rng.normal(0, 4, img.shape), 0, 255).astype(np.uint8)
    return cv2.GaussianBlur(noisy, (3, 3), 0)


def phone_photo(img, rng, angle):
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 0.92)
    out = cv2.warpAffine(img, M, (w, h), borderValue=200)
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    P = cv2.getPerspectiveTransform(src, src + rng.uniform(-50, 50, (4, 2)).astype(np.float32))
    out = cv2.warpPerspective(out, P, (w, h), borderValue=200)
    shade = np.linspace(0.8, 1.0, w)[None, :] * np.linspace(0.9, 1.0, h)[:, None]
    out = np.clip(out.astype(float) * shade + rng.normal(0, 8, out.shape), 0, 255).astype(np.uint8)
    out = cv2.GaussianBlur(out, (5, 5), 1.1)
    _, buf = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)


def low_res(img):
    small = cv2.resize(img, (620, 877), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 45])
    return cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)


def digital_pdf(path, inv, variant):
    c = canvas.Canvas(str(path), pagesize=A4)
    pw, ph = A4
    s = pw / W
    for x, y, t, size, b in layout(inv, variant):
        c.setFont("Helvetica-Bold" if b else "Helvetica", size * s)
        c.drawString(x * s, ph - (y + size) * s, t)
    c.save()


def scanned_pdf(path, png):
    c = canvas.Canvas(str(path), pagesize=A4)
    c.drawImage(str(png), 0, 0, width=A4[0], height=A4[1])
    c.save()


def main():
    OUT.mkdir(exist_ok=True)
    rng = random.Random(42)
    nrng = np.random.default_rng(42)
    truth = []

    def record(fname, kind, inv, variant):
        truth.append({"file": fname, "kind": kind, "variant": variant, "invoice_no": inv["invoice_no"],
                      "date": inv["date"], "vendor": inv["vendor"], "subtotal": inv["subtotal"],
                      "tax": inv["tax"], "total_printed": inv["printed_total"],
                      "items": [(i["description"], i["qty"], i["amount"]) for i in inv["items"]],
                      "arithmetic_ok": abs(inv["subtotal"] + inv["tax"] - inv["printed_total"]) < 0.01})

    inv1 = make_invoice(rng); img1 = draw_pil(layout(inv1, "A"))
    cv2.imwrite(str(OUT / "01_clean_scan.png"), clean_scan(img1, nrng)); record("01_clean_scan.png", "clean scan", inv1, "A")

    inv2 = make_invoice(rng); img2 = draw_pil(layout(inv2, "B"))
    cv2.imwrite(str(OUT / "02_clean_scan_b.png"), clean_scan(img2, nrng)); record("02_clean_scan_b.png", "clean scan", inv2, "B")

    inv3 = make_invoice(rng, error=True); img3 = draw_pil(layout(inv3, "A"))
    cv2.imwrite(str(OUT / "03_clean_scan_wrong_total.png"), clean_scan(img3, nrng))
    record("03_clean_scan_wrong_total.png", "clean scan", inv3, "A")

    inv4 = make_invoice(rng); img4 = draw_pil(layout(inv4, "A"))
    cv2.imwrite(str(OUT / "04_phone_angle.jpg"), phone_photo(img4, nrng, 4.0)); record("04_phone_angle.jpg", "phone photo", inv4, "A")

    inv5 = make_invoice(rng); img5 = draw_pil(layout(inv5, "B"))
    cv2.imwrite(str(OUT / "05_phone_angle_b.jpg"), phone_photo(img5, nrng, -6.0)); record("05_phone_angle_b.jpg", "phone photo", inv5, "B")

    inv6 = make_invoice(rng); img6 = draw_pil(layout(inv6, "A"))
    cv2.imwrite(str(OUT / "06_low_res.jpg"), low_res(img6)); record("06_low_res.jpg", "low resolution", inv6, "A")

    inv7 = make_invoice(rng)
    digital_pdf(OUT / "07_digital.pdf", inv7, "B"); record("07_digital.pdf", "digital PDF", inv7, "B")

    inv8 = make_invoice(rng); img8 = draw_pil(layout(inv8, "A"))
    png8 = OUT / "_tmp8.png"; cv2.imwrite(str(png8), clean_scan(img8, nrng))
    scanned_pdf(OUT / "08_scanned_pdf.pdf", png8); png8.unlink()
    record("08_scanned_pdf.pdf", "scanned PDF (no text layer)", inv8, "A")

    (OUT / "ground_truth.json").write_text(json.dumps(truth, indent=2))
    print(f"wrote {len(truth)} documents to {OUT}/")


if __name__ == "__main__":
    main()
