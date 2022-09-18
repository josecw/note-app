"""
tests root
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from decouple import config

from main import app

BASE_URL = config('BASE_URL')

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    res = await client.get("/")
    
    assert res.status_code == 200
    assert res.json() == {"message": "Note-App is live"}

