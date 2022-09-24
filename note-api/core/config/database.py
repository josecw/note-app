import motor.motor_asyncio
from beanie import init_beanie
import aioredis
from pydantic_aioredis import RedisConfig
from pydantic_aioredis import Store

from core.config import settings
from core.models.note import Note
from core.models.user import User
from core.models.auth import TokenData

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
    # redis = await aioredis.from_url(
    #     f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}?encoding=utf-8", 
    #     password=settings.REDIS_PASS
    # )

    # Redisconfig. Change this configuration to match your redis server
    redis_config = RedisConfig(
        db=5, host=settings.REDIS_HOST, password=settings.REDIS_PASS, port=settings.REDIS_PORT
    )

    # Create the store and register your models
    store = Store(
        name="note-auth", redis_config=redis_config, life_span_in_seconds=settings.JWT_EXPIRY
    )
    store.register_model(TokenData)
    
