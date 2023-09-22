from models.dividends import DividendType
from app.api.v1.schema.request.base import TimeStampRequestSchema


class DividendsRequestSchema(TimeStampRequestSchema):
    amount: int
    organisation_name: str | None = None
    dividend_type: DividendType