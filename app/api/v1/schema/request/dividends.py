from pydantic.schema import date
from pydantic import BaseModel
from models.dividends import DividendType
from app.api.v1.schema.request.base import TimeStampRequestSchema


class DividendsRequestSchema(TimeStampRequestSchema):
    amount: int
    organisation_name: str | None = None
    dividend_type: DividendType
    credited_date: date
    interest_id: str


class DividendGetArgs(BaseModel):
    year: str | None = None
