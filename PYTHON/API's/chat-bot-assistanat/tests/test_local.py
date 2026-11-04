import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from models import CalculatorArgs
from services.tool_service import calculate
from services.invoice_service import regex_invoice


def test_calculator():

    args = CalculatorArgs(
        operation="add",
        a=10,
        b=20
    )

    assert calculate(args) == 30


def test_division():

    args = CalculatorArgs(
        operation="divide",
        a=20,
        b=4
    )

    assert calculate(args) == 5


def test_division_by_zero():

    args = CalculatorArgs(
        operation="divide",
        a=10,
        b=0
    )

    with pytest.raises(ValueError):
        calculate(args)


def test_invoice_regex():

    text = """
    ACME OFFICE SUPPLIES
    Invoice Number: INV-2026-1042
    Date: 20/10/2026
    Grand Total: INR 504.00
    """

    result = regex_invoice(text)

    assert result["invoice_number"] == "INV-2026-1042"
    assert result["total"] == 504.00