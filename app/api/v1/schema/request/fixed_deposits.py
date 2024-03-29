import enum
from pydantic import BaseModel
from pydantic.schema import date
from app.api.v1.schema.request.base import TimeStampRequestSchema


class FixedDepositsRequestSchema(TimeStampRequestSchema):
    bank_name: str
    rate_of_interest: str
    start_date: date
    end_date: date
    maturity_amount: float | None = None
    total_time: str
    remarks: str | None = None
    initial_investment: int


class StatementTypes(enum.Enum):
    PL = "PL"


class FixedDepositGetArgs(BaseModel):
    statement_type: StatementTypes | None = None
    end_date: date | None = None
    maturity_year: int | None = None
    bank: str | None = None
