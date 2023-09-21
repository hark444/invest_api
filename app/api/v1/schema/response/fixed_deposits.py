from pydantic.schema import date
from pydantic import BaseModel
from typing import List
from app.api.v1.schema.response.base import TimeStampResponseSchema


class FixedDepositPLInvestmentSchema(BaseModel):
    initial_investment: int
    total_profit: float | None = None


class FixedDepositsResponseSchema(TimeStampResponseSchema, FixedDepositPLInvestmentSchema):
    bank_name: str
    rate_of_interest: str
    start_date: date
    end_date: date
    maturity_amount: int | None = None
    total_time: str
    remarks: str | None = None
    user_id: int


class AllFixedDepositsResponseSchema(BaseModel):
    data: list[FixedDepositsResponseSchema]
    total: int


class FixedDepositPLStatementResponseSchema(BaseModel):
    data: List[FixedDepositsResponseSchema]
    total_investment: int
    total_profit: int

    class Config:
        orm_mode = True
