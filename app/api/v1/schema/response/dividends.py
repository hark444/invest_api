from app.api.v1.schema.response.base import TimeStampResponseSchema


class DividendsResponseSchema(TimeStampResponseSchema):
    amount: int
    organisation_name: str | None = None
    dividend_type: str
    user_id: int
