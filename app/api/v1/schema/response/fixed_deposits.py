from pydantic.schema import date
from app.api.v1.schema.response.base import TimeStampResponseSchema


class FixedDepositsResponseSchema(TimeStampResponseSchema):
    bank_name: str
    rate_of_interest: str
    start_date: date
    end_date: date
    maturity_amount: int | None = None
    total_time: str
    remarks: str | None = None
    initial_investment: int
    user_id: int
