import motor.motor_asyncio
from beanie import init_beanie
import aioredis

from core.config import settings
from core.models.note import Note
from core.models.user import User

mongo_uri = "mongodb+srv://{user}:{password}@{host}/{db}".format(
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    db=settings.DB_NAME
)

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri,
                                                connectTimeoutMS=settings.DB_TIMEOUT,
                                                socketTimeoutMS=settings.DB_TIMEOUT,
                                                w='majority',
                                                retryWrites=True,
                                                readPreference='secondary')

db = client[settings.DB_NAME]


async def init_db(db):

    await init_beanie(database=db,
                      document_models=[
                          Note,
                          User
                      ]
                      )


async def redis_pool(db: int = 0):
    """

    """
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}?encoding=utf-8", 
        password=settings.REDIS_PASS
    )
    return redis
