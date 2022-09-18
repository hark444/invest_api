from pydantic import BaseModel
from typing import List
from app.api.v1.schema.response.party import PartyResponseSchema
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.schema.response.base import TimeStampResponseSchema


class PartiesAttendedResponseSchema(TimeStampResponseSchema):
    user_id: int
    user: UserResponseSchema
    party_id: int
    party: PartyResponseSchema
    rating: float
    comment: str | None = None
    approved: bool


class AllPartiesAttendedResponseSchema(BaseModel):
    total: int
    data: list[PartiesAttendedResponseSchema]
