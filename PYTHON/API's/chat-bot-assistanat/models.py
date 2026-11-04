from pydantic import BaseModel, Field


class InvoiceFields(BaseModel):

    invoice_number: str | None = None
    invoice_date: str | None = None
    vendor: str | None = None
    total: float | None = None
    currency: str | None = None


class CalculatorArgs(BaseModel):

    operation: str = Field(
        pattern="^(add|subtract|multiply|divide)$"
    )

    a: float = Field(
        ge=-1_000_000,
        le=1_000_000
    )

    b: float = Field(
        ge=-1_000_000,
        le=1_000_000
    )