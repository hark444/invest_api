import enum

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Float, String, DateTime, Enum
from models.user import UserModel
from models.base_models import TimeStampBaseModel
# from enum import Enum
from datetime import datetime


class MFInvestmentTypes(str, enum.Enum):
    SIP = "SIP"
    LUMPSUM = "LUMPSUM"
    REGULAR = "REGULAR"


class MFInvestments(TimeStampBaseModel):
    __tablename__ = "mf_investments"

    id = Column(Integer, primary_key=True, index=True)
    investment_amount = Column(Float, nullable=False)
    investment_date = Column(DateTime, default=datetime.now())
    remarks = Column(String, nullable=True)


class MutualFunds(TimeStampBaseModel):
    __tablename__ = "mutual_funds"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    investment_type = Column(Enum(MFInvestmentTypes), nullable=False, server_default="REGULAR")
    broker_name = Column(String, nullable=True)
    total_investment = Column(Float, default=0.0)
    mf_investments_id = Column(BigInteger, ForeignKey("mf_investments.id"))
    mf_investments = relationship(MFInvestments)
    current_nav = Column(Float, nullable=True)
    return_on_investment = Column(Float, nullable=True)
    cagr = Column(Float, nullable=True)
