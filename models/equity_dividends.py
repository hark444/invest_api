import enum
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class Party(Base):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    reason = Column(String)
    proposed_date = Column(DateTime, default=datetime.now(), nullable=False)
    guests_invited = Column(Integer, nullable=False, default=0)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
    party_date = Column(DateTime, nullable=True)
    party_place = Column(String, nullable=True)
    ratings = Column(Float, nullable=True)
    approved = Column(Boolean, nullable=False, default=False)
