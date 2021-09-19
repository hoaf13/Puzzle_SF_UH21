from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import datetime
import patient as pt
import patientDB
import apartmentCalendar as ap
import apartmentDB

router = APIRouter()

@router.post("/patient", response_description="Patient data added into the database")
async def add_student_data(patient: pt.PatientSchema = Body(...)):
    patient = jsonable_encoder(patient)
    updateStatus = False
    apartment = await apartmentDB.get_apartment(patient["apartmentName"])
    for dateIndex in range(len(apartment["dateCalendars"])):
        date = apartment["dateCalendars"][dateIndex]
        if date["date"] == patient["appointmentDate"]:
            break
    apartment["dateCalendars"][dateIndex]["startTimes"].append(patient["startAppointmentTime"])
    updateStatus = await apartmentDB.update_apartment(apartment)
    if updateStatus:
        new_patient = await patientDB.add_patient(patient)
        return pt.ResponseModel(new_patient, "Patient added successfully.")
    else:
        return "Can't update apartment calendar"

@router.post("/apartment", response_description="Apartment data added into the database")
async def add_apartment_data(apartment: ap.ApartmentCalendarSchema = Body(...)):
    apartment = jsonable_encoder(apartment)
    new_apartment= await apartmentDB.add_apartment(apartment)
    return pt.ResponseModel(new_apartment, "Apartment added successfully.")

@router.get("/apartment/this_week/{name}", response_description="Get free day of apartment in this week")
async def get_all(name):
    return await apartmentDB.get_lis_free_appartment_this_week(name)

@router.get("/apartment/next_week/{name}", response_description="Get free day of apartment in next week")
async def get_all(name):
    return await apartmentDB.get_lis_free_appartment_next_week(name)

@router.get("/apartment/{name}/{date_order}/{month_order}/{year_order}", response_description=" get free calendar in a day")
async def get_free_calendar(name, date_order, month_order, year_order):
    apartment = await apartmentDB.get_apartment(name)
    freeCalendar = []
    dateCalenders = apartment["dateCalendars"]
    deltaTime = apartment["deltaTime"]
    considerTime = apartment["openTime"]
    closeTime = apartment["closeTime"]
    timeBusyIndex = 0
    day_order = month_order+"/"+date_order+ "/" + year_order
    while closeTime - considerTime >= deltaTime:
        freeCalendar.append(considerTime)
        considerTime += deltaTime
    print(freeCalendar)
    for dateIndex in range(len(dateCalenders)):
        date = dateCalenders[dateIndex]
        if (date["date"]) == day_order:
            for busyTime in date["startTimes"]:
                print(type(busyTime))
                freeCalendar.remove(busyTime)
            break
            
    
    return {
        "free_calendar": freeCalendar
    }