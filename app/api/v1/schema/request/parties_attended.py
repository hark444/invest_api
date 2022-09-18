from pydantic.schema import datetime
from app.api.v1.schema.request.base import TimeStampRequestSchema


class PartiesAttendedRequestSchema(TimeStampRequestSchema):
    party_id: int
    rating: float
    approved: bool = False
    comment: str | None = None
