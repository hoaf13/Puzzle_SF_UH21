from typing import Optional

from pydantic import BaseModel, Field
import datetime

class DateCalendarSchema(BaseModel):
    date: str= Field(...)
    orderInWeek: int = Field(...)
    startTimes: list[float] = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "date": datetime.datetime.now().strftime("%m/%d/%Y"),
                "orderInWeek": 2,
                "startTimes": []
            }
        }

