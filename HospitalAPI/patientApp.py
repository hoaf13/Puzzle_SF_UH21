from fastapi import FastAPI
import patientRoutes

app = FastAPI()
app.include_router(patientRoutes.router, tags=["Hospital"], prefix="/hospital")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}