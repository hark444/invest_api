from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class DepositsBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)
    rate_of_interest = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now(), nullable=False)
    end_date = Column(DateTime, default=datetime.now(), nullable=False)
    maturity_amount = Column(Integer, nullable=True, doc="Maturity Amount of the Instrument")
    total_time = Column(
        String, nullable=True,
        doc="Total investment time of the instrument. This should ideally be converted into number of days."
    )
    remarks = Column(String, nullable=True)


class TimeStampBaseModel(Base):
    __abstract__ = True

    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, onupdate=datetime.now(), nullable=True)