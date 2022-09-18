from pydantic import BaseModel
from datetime import datetime


class TimeStampRequestSchema(BaseModel):
    created_on: datetime | None = datetime.now()
    last_modified_on: datetime | None = None
