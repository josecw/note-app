"""
Pytest fixtures
"""
import pytest
import pytest_asyncio
from typing import Iterator
import asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from decouple import config 

from main import app
from core.models.user import User

BASE_URL = config('BASE_URL')
USER1 = config("TEST_USER_1")
USER2 = config("TEST_USER_2")
PWD = config('CORRECT_PWD')

@pytest_asyncio.fixture
async def client() -> Iterator[AsyncClient]:
    """
    Create an instance of the client.
    :return: yield HTTP client.
    """
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url=BASE_URL) as _client:
            try:
                yield _client
            except Exception as e:  
                print(e)

@pytest_asyncio.fixture
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop

    pending = asyncio.tasks.all_tasks(loop)
    loop.run_until_complete(asyncio.gather(*pending))
    loop.run_until_complete(asyncio.sleep(0.5))

    loop.close()

@pytest_asyncio.fixture
async def auth_payload_a(client: AsyncClient):
    """Returns the login auth payload for an email"""
    data = {"username": USER1, "password": PWD}
    res = await client.post("/v1/login", json=data)
    
    return res.json()

@pytest_asyncio.fixture
async def auth_payload_b(client: AsyncClient):
    """Returns the login auth payload for an email"""
    data = {"username": USER2, "password": PWD}
    res = await client.post("/v1/login", json=data)
    
    return res.json()