from models.mutual_funds import MFInvestmentTypes
from pydantic import BaseModel
from pydantic.schema import date
from app.api.v1.schema.request.base import TimeStampRequestSchema


class MFRequestSchema(TimeStampRequestSchema):
    broker_name: str
    name: str
    start_date: date
    investment_amount: float | None = None
    remarks: str | None = None
    investment_type: MFInvestmentTypes


class FixedDepositGetArgs(BaseModel):
    end_date: date | None = None
    maturity_year: int | None = None
    bank: str | None = None
