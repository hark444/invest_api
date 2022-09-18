import enum
from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from datetime import datetime
from models import Base


class RoleTypeEnum(str, enum.Enum):
    admin = "admin"
    superuser = "superuser"
    regular = "regular"


class UserModel(Base):
    __tablename__ = "account_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(Enum(RoleTypeEnum), nullable=False, server_default="regular")
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
