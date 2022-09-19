"""
Pytest fixtures
"""
import pytest
import pytest_asyncio
from typing import Iterator
import asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app
from core.models.user import User
from tests.settings import BASE_URL, USER1, USER2, PWD


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

@pytest_asyncio.fixture(scope="session")
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
async def auth_header_a(client: AsyncClient, auth_payload_a):
    """Returns authorizatio header of tester A"""
    headers_a = {"AUTHORIZATION": f"Bearer {auth_payload_a.get('token')}"}

    return headers_a

@pytest_asyncio.fixture
async def auth_payload_b(client: AsyncClient):
    """Returns the login auth payload for an email"""
    data = {"username": USER2, "password": PWD}
    res = await client.post("/v1/login", json=data)
    
    return res.json()

@pytest_asyncio.fixture
async def auth_header_b(client: AsyncClient, auth_payload_b):
    """Returns authorizatio header of tester B"""
    headers_b = {"AUTHORIZATION": f"Bearer {auth_payload_b.get('token')}"}

    return headers_b


@pytest_asyncio.fixture
async def a_random_note_id(client: AsyncClient, auth_header_a):
    """Return random note id from tester A to tester B"""

    # Get Tester A Data
    res = await client.get('/v1/note/', headers=auth_header_a)
    id = res.json()[-1].get('_id')

    return id

@pytest_asyncio.fixture
async def a_random_note_tag(client: AsyncClient, auth_header_a):
    """Return random note id from tester A to tester B"""

    # Get Tester A Data
    res = await client.get('/v1/note/', headers=auth_header_a)
    tag = res.json()[-1].get('tags')[0]

    return tag