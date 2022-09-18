from pydantic import BaseModel
from models.user import RoleTypeEnum


class RoleTypeSchema(BaseModel):
    role: RoleTypeEnum
