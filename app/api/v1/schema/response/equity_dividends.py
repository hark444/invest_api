from pydantic.schema import date
from app.api.v1.schema.response.base import TimeStampResponseSchema


class EquityDividendsResponseSchema(TimeStampResponseSchema):
    user_id: int
    amount: int
    credited_date: date
    equity: str
    shares: int
    ISIN: str
