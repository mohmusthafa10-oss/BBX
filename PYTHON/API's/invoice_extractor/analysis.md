# Where each method failed, and what I would ship

**Regex anchors** failed silently on garbled characters. On `01_clean_scan`, OCR read 652.22 as "652:22", so that row vanished from the regex output and the item sum stopped matching the subtotal. The item pattern also requires an integer quantity, so "vf" in place of "19" removed another row. One character error in a line is enough to lose the line.

**Position extraction** had the worst silent failure. When the amount token was garbled, the rightmost number on the row was the unit price, so the row reported a plausible but wrong amount. Reading only the Amount column fixed that. It still over-counts on `05_phone_angle_b` (6 rows against 5), probably where OCR split one row across two lines. I did not fix that case. The disagreement check routes it to review.

**Preprocessing** helped phone photos (mean confidence +26.7 and +9.0), slightly hurt clean scans (-1 to -4), and badly hurt the low-resolution scan (-44.9). Binarisation erases thin strokes when the source is already small. Character counts are misleading: the phone photo's raw OCR produced 863 characters, most of it noise.

**Confidence does not predict correctness.** `01_clean_scan` scored 92 and still had three of its five items.

**What I would ship** for 10,000 invoices a day: a deterministic pipeline that reads the text layer when one exists, uses OCR only for scans, and gates every result on arithmetic checks. Validation is the reliable signal here. OCR confidence is not. I would not ship an LLM-only extractor, because it can return fluent, confident values that look right and are wrong. I would use an LLM as a second reader over the same text, accept a result only when it agrees with the deterministic extraction and the arithmetic holds, and send every disagreement to a person.

**What a confident error costs.** At 10,000 invoices a day, a 0.5% silent error rate means 50 wrong records daily. A misread total can overpay or duplicate a payment. A misread bank detail can send money to a fraudster. Each error then needs recovery, an audit trail and sometimes regulatory reporting. Routing to review is slower, but a document waiting in a queue can be fixed, and a wrong payment often cannot be recalled.

**Limits.** These results come from 8 synthetic documents, one template family and one OCR engine. They show failure modes, not production accuracy. The 0.5% rate above is illustrative, not measured.
