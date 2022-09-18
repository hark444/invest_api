import enum
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    DATE,
    BigInteger,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class EquityDividends(Base):
    __tablename__ = "equity_dividends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    amount = Column(Float, nullable=False, default=0)
    credited_date = Column(DATE, default=datetime.now())
    equity = Column(String, nullable=False)
    shares = Column(Integer, nullable=False, default=0)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
