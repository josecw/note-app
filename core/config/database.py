import motor.motor_asyncio
from beanie import init_beanie

from core.config.settings import db_host, db_name, db_pass, db_user, db_socket_timeout, db_connect_timeout
from core.models.note import Note
from core.models.user import User

mongo_uri = "mongodb+srv://{user}:{password}@{host}/{db}".format(
    user=db_user,
    password=db_pass,
    host=db_host,
    db=db_name
)

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri,
                                                    connectTimeoutMS=db_connect_timeout,
                                                    socketTimeoutMS=db_socket_timeout,
                                                    w='majority',
                                                    retryWrites=True,
                                                    readPreference='secondary')

db = client[db_name]

async def init_db(db):
    
    await init_beanie(database=db,
        document_models=[
            Note,
            User
        ]
    )