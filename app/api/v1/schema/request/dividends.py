from pydantic.schema import date
from pydantic import validator, ValidationError
from models import get_db
from models.dividends import Dividends
from fastapi import Depends
from sqlalchemy.orm import Session
from models.dividends import DividendType
from app.api.v1.schema.request.base import TimeStampRequestSchema


class DividendsRequestSchema(TimeStampRequestSchema):
    amount: int
    organisation_name: str | None = None
    dividend_type: DividendType
    credited_date: date
    interest_id: str
