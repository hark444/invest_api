from pydantic import BaseModel
from pydantic.schema import date
from app.api.v1.schema.response.base import TimeStampResponseSchema


class DividendsResponseSchema(TimeStampResponseSchema):
    amount: int
    organisation_name: str | None = None
    dividend_type: str
    user_id: int
    credited_date: date


class AllDividendsResponseSchema(BaseModel):
    data: list[DividendsResponseSchema]
    total: int
    total_amount: int
