import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from assistant import CalculatorArgs, calculate, regex_invoice

def test_calculator():
    assert calculate(CalculatorArgs(operation="divide",a=184.5,b=3)) == 61.5
    assert calculate(CalculatorArgs(operation="add",a=61.5,b=27)) == 88.5

def test_divide_zero():
    try: calculate(CalculatorArgs(operation="divide",a=1,b=0))
    except ValueError: return
    assert False

def test_regex_fixture():
    from pathlib import Path
    data=(Path(__file__).parents[1]/"data"/"invoice_ocr.txt").read_text()
    result=regex_invoice(data)
    assert result["invoice_number"] == "INV-2026-1042"
    assert result["total"] == 504.0
