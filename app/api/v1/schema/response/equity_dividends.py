from pydantic.schema import date, List
from pydantic import BaseModel
from app.api.v1.schema.response.base import TimeStampResponseSchema


class EquityDividendsResponseSchema(TimeStampResponseSchema):
    user_id: int
    amount: int
    credited_date: date
    equity: str
    shares: int
    ISIN: str


class EquityDividendsAllResponseSchema(BaseModel):
    total: int
    total_amount: float
    data: list[EquityDividendsResponseSchema]