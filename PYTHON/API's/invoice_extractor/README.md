# Invoice extractor

Extracts invoice fields from PDFs and images, checks them arithmetically, and routes each document to `accepted/` or `needs_review/`.

## Files

- `make_samples.py`: generates 8 **synthetic** invoices with ground truth in `samples/`. No real invoices were available, so the samples cover the document types but not real-world variation.
- `invoice_extractor.py`: the pipeline (text-layer detection, preprocessing, OCR with and without preprocessing, regex and position extraction, validation, routing).
- `evaluate.py`: scores raw and preprocessed OCR field extraction against ground truth.
- `analysis.md`: where each method failed, and what I would ship.

## Run

    pip install opencv-python-headless numpy pdfplumber pytesseract pillow reportlab
    python3 make_samples.py
    python3 invoice_extractor.py samples --out out
    python3 evaluate.py --samples samples --out out

Requires the Tesseract binary on the PATH.

## Outputs (in `out/`)

- `results.csv`, `results.md`: extracted fields, confidence, validation result and route per document.
- `comparison.csv`: OCR character counts and mean word confidence, raw versus preprocessed.
- `evaluation.md`: field-level accuracy against ground truth.
- `intermediate/<doc>/`: grayscale, threshold, deskew and denoise images for each document.
- `ocr/`: every OCR text (raw, preprocessed, and text layer where present).
- `fields/`: field extraction for each OCR output.
- `accepted/`, `needs_review/`: copies of each document, with a `.reasons.json` file for every review.
- `run.log`: which path ran for each document, and why.

## Routing rules

A document goes to `needs_review/` if any of these hold:

1. Mean OCR word confidence is below 80 (OCR path only).
2. Any required field is missing.
3. Line items do not sum to the subtotal, or any line amount is unreadable.
4. Subtotal + tax does not equal the total.
5. The date cannot be parsed or is implausible.
6. Regex and position extraction disagree.

The date parser assumes day-first (DD/MM/YYYY) for numeric dates, matching the generator. Confirm this against your real documents before using the system.
