from typing import Optional

from pydantic import BaseModel, Field
import datetime
import dateCalendar

class ApartmentCalendarSchema(BaseModel):
    name: str = Field(...)
    deltaTime: float = Field(...)
    openTime: float = Field(...)
    closeTime: float = Field(...)
    dateCalendars: list[dateCalendar.DateCalendarSchema] = Field(...)

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}