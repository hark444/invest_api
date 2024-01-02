import enum

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Float, String, DateTime, Enum
from models.user import UserModel
from models.base_models import TimeStampBaseModel
from enum import Enum


class MFInvestmentTypes(str, enum.Enum):
    SIP = "SIP"
    LUMPSUM = "LUMPSUM"
    REGULAR = "REGULAR"


class MutualFunds(TimeStampBaseModel):
    __tablename__ = "mutual_funds"

    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    investment_type = Column(Enum(MFInvestmentTypes), nullable=False, server_default="REGULAR")
    broker_name = Column(String, nullable=True)
    total_investment = Column(Float, default=0.0)
    investments = relationship("MFInvestments", back_populates="mf_investments")

#
# class MFInvestments(TimeStampBaseModel):

