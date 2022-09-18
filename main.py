from beanie import init_beanie
from fastapi import FastAPI

from core.routes.v1.api import api_router as v1_api
from core.config.database import init_db, db
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db(db)

app.include_router(v1_api, prefix='/v1')

@app.get("/", include_in_schema=False)
async def read_root() -> dict:
    return {"message": "Note App is up"}