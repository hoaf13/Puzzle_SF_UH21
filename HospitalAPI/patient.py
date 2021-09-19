from typing import Optional

from pydantic import BaseModel, EmailStr, Field
import datetime

class PatientSchema(BaseModel):
    fullname: str = Field(...)
    phoneNumber: int = Field(...)
    gender: str = Field(...)
    piority: bool = Field(...)
    startAppointmentTime: float = Field(...)
    appointmentDate: str = Field(...)
    apartmentName: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "phoneNumber": 412323,
                "gender": "male",
                "piority": True,
                "startAppointmentTime": 9,
                "appointmentDate": datetime.datetime.now().strftime("%m/%d/%Y"),
                "apartmentName": "ngoai khoa",
            }
        }
class UpdatePatientModel(BaseModel):
    fullname: Optional[str]
    phoneNumber: Optional[int]
    gender: Optional[str]
    piority: Optional[bool]
    startAppointmentTime: Optional[float]
    appointmentDate: Optional[str]
    apartmentName: Optional[str]
    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "phoneNumber": 412323,
                "gender": "male",
                "piority": True,
                "startAppointmentTime": 9,
                "appointmentDate": datetime.datetime.now().strftime("%m/%d/%Y"),
                "apartmentName": "ngoai khoa",
            }
        }
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}