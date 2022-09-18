"""
tests Authentication
"""

from datetime import datetime
import pytest
from httpx import AsyncClient
from decouple import config

USER1 = config("TEST_USER_1")
PWD = config('CORRECT_PWD')

@pytest.mark.asyncio
async def test_login(client:AsyncClient) -> None:
    
    data = {
        "username": USER1,
        "password": PWD
    }

    response = await client.post("/v1/login", json=data)

    assert response.status_code == 200
    assert response.json().get('token') is not None

@pytest.mark.asyncio
async def test_logout(client:AsyncClient) -> None:
    """Test Logout"""
    data = {
        "username": USER1
    }

    res = await client.post("/v1/logout", json=data)

    assert res.status_code == 200
    assert res.text == ''
    

@pytest.mark.asyncio
async def test_invalid_token(client:AsyncClient) -> None:
    """Test Invalid Bearer"""
    headers = {"AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbG"}
    res = await client.get("/v1/user/current_user", headers=headers)
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_invalid_token(client:AsyncClient) -> None:
    """Test Invalid Bearer"""
    headers = {"AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbG"}
    res = await client.get("/v1/user/current_user", headers=headers)
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_valid_token(client:AsyncClient, auth_payload_a) -> None:
    """Test Valid Bearer"""
    headers = {"AUTHORIZATION": f"Bearer {auth_payload_a.get('token')}"}
    res = await client.get("/v1/user/current_user", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data.get('username') == USER1
    assert data.get('last_logon_dt') is not None