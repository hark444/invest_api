from pydantic.schema import datetime
from app.api.v1.schema.request.base import TimeStampRequestSchema


class PartyRequestSchema(TimeStampRequestSchema):
    reason: str = None
    proposed_date: datetime
    guests_invited: int
    party_date: datetime | None = None
    party_place: str | None = None
    ratings: float | None = None
    approved: bool = False
