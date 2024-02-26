from pydantic.schema import date
from app.api.v1.schema.response.base import TimeStampResponseSchema
from models.mutual_funds import MFInvestmentTypes


class MFResponseSchema(TimeStampResponseSchema):
    broker_name: str
    name: str
    start_date: date
    investment_amount: float | None = None
    remarks: str | None = None
    investment_type: MFInvestmentTypes
    user_id: int
    total_investment: float | None = None
    current_nav: float | None = None
    return_on_investment: str | None = None
    cagr: str | None = None