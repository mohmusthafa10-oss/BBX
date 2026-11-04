import re
import json

from google.genai import types

from config import MODEL
from models import InvoiceFields
from services.gemini_client import retry_call


def regex_invoice(text):

    def find(pattern):

        match = re.search(
            pattern,
            text,
            re.I | re.M
        )

        return match.group(1).strip() if match else None

    total = find(
        r"(?:grand\s+)?total\s*[:\-]?\s*"
        r"(?:AED|USD|INR|₹|\$)?\s*([\d,]+\.\d{2})"
    )

    currency_match = re.search(
        r"\b(AED|USD|INR)\b|([₹$])",
        text,
        re.I
    )

    currency = None

    if currency_match:

        currency = (
            currency_match.group(1)
            or currency_match.group(2)
        )

    return {

        "invoice_number": find(
            r"invoice\s*(?:no|number|#)\s*[:#-]?\s*([A-Z0-9/-]+)"
        ),

        "invoice_date": find(
            r"date\s*[:\-]?\s*(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})"
        ),

        "vendor": find(
            r"(?m)^([A-Z][A-Za-z &.,'-]{2,})$"
        ),

        "total": (
            float(total.replace(",", ""))
            if total else None
        ),

        "currency": currency
    }


def extract_invoice(client, path, usage_tracker):

    raw_text = path.read_text(
        encoding="utf-8"
    )

    config = types.GenerateContentConfig(

        system_instruction=(
            "Extract invoice fields from the supplied OCR text. "
            "Return null for missing values. "
            "Never invent missing information."
        ),

        response_mime_type="application/json",

        response_json_schema=InvoiceFields.model_json_schema(),

        max_output_tokens=300
    )

    response = retry_call(
        lambda: client.models.generate_content(

            model=MODEL,

            contents=raw_text,

            config=config
        )
    )

    if not response.text:

        print("[invoice] No structured response returned.")

        return

    extracted = InvoiceFields.model_validate_json(
        response.text
    )

    regex_result = regex_invoice(raw_text)

    print("\n[Gemini structured output]")

    print(
        extracted.model_dump_json(indent=2)
    )

    print("\n[Regex output]")

    print(
        json.dumps(regex_result, indent=2)
    )

    print("\n[comparison] Review differences manually.")

    usage_tracker.report(
        response.usage_metadata
    )