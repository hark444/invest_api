from pydantic.schema import datetime
from app.api.v1.schema.response.base import TimeStampResponseSchema


class PartyResponseSchema(TimeStampResponseSchema):
    user_id: int
    reason: str | None
    proposed_date: datetime
    guests_invited: int
    party_date: datetime | None
    party_place: str | None
    ratings: float | None
    approved: bool
