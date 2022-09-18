from pydantic import BaseModel
from datetime import datetime


class TimeStampResponseSchema(BaseModel):
    id: int
    created_on: datetime | None = datetime.now()
    last_modified_on: datetime | None = None

    class Config:
        orm_mode = True
