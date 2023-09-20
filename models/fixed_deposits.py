from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Float
from models.user import UserModel
from models.base_models import DepositsBaseModel, TimeStampBaseModel


class FixedDeposits(DepositsBaseModel, TimeStampBaseModel):
    __tablename__ = "fixed_deposits"

    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    initial_investment = Column(Integer, nullable=False, doc="Initial amount that was invested as FD")
    total_profit = Column(Float, nullable=True)
