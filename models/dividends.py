from sqlalchemy import (
    Column,
    Integer,
    String,
    DATE,
    BigInteger,
    ForeignKey,
    Float,
    Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models.user import UserModel
from models.base_models import TimeStampBaseModel
import enum


class DividendType(str, enum.Enum):
    FD = 'FD'
    SBI = 'SBI'
    SGB = 'SGB'


class Dividends(TimeStampBaseModel):
    __tablename__ = "dividends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    amount = Column(Float, nullable=False, default=0)
    credited_date = Column(DATE, default=datetime.now())
    dividend_type = Column(Enum(DividendType), server_default="FD")
    organisation_name = Column(String, nullable=False)
