import motor.motor_asyncio
from bson.objectid import ObjectId
import datetime
MONGO_DETAILS = "mongodb+srv://kudo313:kudo_321@cluster1.mza5o.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.hospitals

apartment_collection = database.get_collection("apartment")

def apartment_helper(apartment) -> dict:
    return {
        "id": str(apartment["_id"]),
        "name": apartment["name"],
        "deltaTime": str(apartment["deltaTime"]),
        "dateCalendars": apartment["dateCalendars"],
        "openTime": apartment["openTime"],
        "closeTime": apartment["closeTime"],
    }

async def add_apartment(apartment_data: dict) -> dict:
    apartments = await apartment_collection.insert_one(apartment_data)
    new_apartment = await apartment_collection.find_one({"_id": apartments.inserted_id})
    return apartment_helper(new_apartment)

async def get_lis_free_appartment_this_week(apartment_name):
    apartment = await apartment_collection.find_one({"name": apartment_name})
    if apartment:
        today = datetime.datetime.now()
        weekDay = today+ datetime.timedelta(days= 6 - today.weekday())
        format = "%m/%d/%Y"
        deltaTime = apartment["deltaTime"]
        ListFreeDay = []
        FreeDay = {}
        status = False
        for dateIndex in range(len(apartment["dateCalendars"])):
            FreeDay = {}
            date = apartment["dateCalendars"][dateIndex]
            day = date["date"]
            if datetime.datetime.strptime(day,format) < today:
                continue
            order = date["orderInWeek"]
            ListStartTime = date["startTimes"]
            sizeOfListStartTime = len(ListStartTime)
            print(datetime.datetime.strptime(day,format).strftime("%A"))
            print(weekDay.strftime("%A"))
            if datetime.datetime.strptime(day,format) < weekDay:
                if sizeOfListStartTime < (apartment["closeTime"] - apartment["openTime"])/deltaTime:
                    status = True
                    FreeDay["date"] = day
                    FreeDay["order"] = order
                    ListFreeDay.append(FreeDay)
            else:
                break
        return {
            "FreeStatus": status,
            "ListFreeDay": ListFreeDay,
        }
    else:
        return "Can not find apartment"

async def get_lis_free_appartment_next_week(apartment_name):
    apartment = await apartment_collection.find_one({"name": apartment_name})
    if apartment:
        today = datetime.datetime.now()
        weekDay = today+ datetime.timedelta(days= 6 - today.weekday())
        nextWeekDay = today+ datetime.timedelta(days= 13 - today.weekday())
        format = "%m/%d/%Y"
        deltaTime = apartment["deltaTime"]
        ListFreeDay = []
        FreeDay = {}
        status = False
        for dateIndex in range(len(apartment["dateCalendars"])):
            date = apartment["dateCalendars"][dateIndex]
            day = date["date"]
            if datetime.datetime.strptime(day,format) < today:
                continue
            order = date["orderInWeek"]
            ListStartTime = date["startTimes"]
            sizeOfListStartTime = len(ListStartTime)
            if datetime.datetime.strptime(day,format) < weekDay:
                pass
            else:
                break
        firstIndexInNextWeek = dateIndex + 1
        for dateIndex in range(firstIndexInNextWeek,len(apartment["dateCalendars"])):
            FreeDay = {}
            date = apartment["dateCalendars"][dateIndex]
            day = date["date"]
            order = date["orderInWeek"]
            ListStartTime = date["startTimes"]
            sizeOfListStartTime = len(ListStartTime)
            if datetime.datetime.strptime(day,format).strftime("%A") != nextWeekDay.strftime("%A"):
                if sizeOfListStartTime < (apartment["closeTime"] - apartment["openTime"])/deltaTime:
                    status = True
                    FreeDay["date"] = day
                    FreeDay["order"] = order
                    print(FreeDay)
                    ListFreeDay.append(FreeDay)
            else:
                break
        return {
            "FreeStatus": status,
            "ListFreeDay": ListFreeDay,
        }
    else:
        return "Can not find apartment"

async def get_apartment(apartment_name):
    apartment = await  apartment_collection.find_one({"name":apartment_name})
    if apartment:
        return (apartment)

async def update_apartment(apartment):
    if len(apartment) < 1:
        return False
    id = apartment["_id"]
    apartment = await apartment_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": apartment}
    )
    return True
