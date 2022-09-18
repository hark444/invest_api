from pydantic.schema import date
from app.api.v1.schema.request.base import TimeStampRequestSchema


class EquityDividendsRequestSchema(TimeStampRequestSchema):
    amount: int
    credited_date: date
    equity: str
    shares: int
    ISIN: str


class EquityDividendsXlsxRequestSchema(TimeStampRequestSchema):
    file_path: str
    error_file_path: str | None = None
