from fastapi import FastAPI
from resources import routes
from db import database

app = FastAPI()
app.include_router(routes.api_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
