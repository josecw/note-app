from fastapi import FastAPI
import uvicorn

from core.routes.v1.api import api_router as v1_api
from core.config.database import init_db, db, redis_pool
from core.config import settings

app = FastAPI()
app.db = db


@app.on_event("startup")
async def on_startup():
    await init_db(app.db)
    app.state.redis = await redis_pool()

app.include_router(v1_api, prefix='/v1')


@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {"message": "Note-App is live"}

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.HOST,
                reload=settings.DEBUG_MODE,
                port=settings.PORT,
                log_level=settings.LOG_LEVEL
                )
