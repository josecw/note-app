"""
tests Note
"""

from datetime import datetime
import pytest
from httpx import AsyncClient
from decouple import config
import json

from core.models.note import Note
from core.config.database import db

f_create = open('tests/data/create_data.json')
create_data = json.load(f_create)

f_update = open('tests/data/update_data.json')
update_data = json.load(f_update)

@pytest.mark.asyncio
async def test_note_create(client:AsyncClient, auth_header_a, auth_header_b) -> None:
    """Test Note Creation"""
    
    # Clear Test User Data
    res = await client.delete(f"/v1/note", headers=auth_header_a)
    assert res.status_code == 204
    assert res.text == ''

    # Clear Test User Data
    res = await client.delete(f"/v1/note", headers=auth_header_b)
    assert res.status_code == 204
    assert res.text == ''

    res = await client.get('/v1/note/', headers=auth_header_a)
    assert len(res.json()) == 0 # Ensure User A Content all delete

    # Test Create
    for note in create_data:
        res = await client.post('/v1/note/', headers=auth_header_a, json=note)
        assert res.status_code == 200
        assert res.json().get('content') == note.get('content')
        assert res.json().get('tags') == note.get('tags')


@pytest.mark.asyncio
async def test_note_list(client:AsyncClient, auth_header_a) -> None:
    """Test Note Creation"""

    # Test List data created by A
    res = await client.get('/v1/note/', headers=auth_header_a)
    
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    for i in res.json(): assert isinstance(i, dict)
    assert len(res.json()) == len(create_data)


@pytest.mark.asyncio
async def test_note_get_no_access(client:AsyncClient, auth_header_b, a_random_note_id) -> None:
    """Test B No Access get A items"""

    res = await client.get(f'/v1/note/{a_random_note_id}', headers=auth_header_b)

    assert res.status_code == 404 # No access

@pytest.mark.asyncio
async def test_note_upd_no_access(client:AsyncClient, auth_header_b, a_random_note_id) -> None:
    """Test B No Access update A items"""

    res = await client.post(f'/v1/note/{a_random_note_id}', headers=auth_header_b, json=update_data)

    assert res.status_code == 404 # No access

@pytest.mark.asyncio
async def test_note_del_no_access(client:AsyncClient, auth_header_b, a_random_note_id) -> None:
    """Test B No Access delete A items"""

    res = await client.delete(f'/v1/note/{a_random_note_id}', headers=auth_header_b)

    assert res.status_code == 404 # No access

@pytest.mark.asyncio
async def test_note_list_no_access(client:AsyncClient, auth_header_b) -> None:
    """Test B No Access list A items"""
    # Test List data created by A using B
    res = await client.get('/v1/note/', headers=auth_header_b)

    assert res.status_code == 200
    assert len(res.json()) == 0

@pytest.mark.asyncio
async def test_note_get_tag_no_access(client:AsyncClient, auth_header_b, a_random_note_tag) -> None:
    """Test B No Access get A tags"""
    # Test list-by-tag created by A using B
    res = await client.get(f'/v1/note/tag/{a_random_note_tag}', headers=auth_header_b)
    
    assert res.status_code == 200 # Get Successful
    assert len(res.json()) == 0 # But Empty

@pytest.mark.asyncio
async def test_note_get_tag_no_access(client:AsyncClient, auth_header_b) -> None:
    """Test B No Access list A tags"""
    # Test list-all-tag using B
    res = await client.get(f'/v1/tags/', headers=auth_header_b)
    assert res.status_code == 200 # Get Successfulauth_header_b
    assert len(res.json()) == 0 # But Empty

@pytest.mark.asyncio
async def test_note_get(client:AsyncClient, auth_header_a, a_random_note_id) -> None:
    """Test Get Note"""
    
    res = await client.get(f'/v1/note/{a_random_note_id}', headers=auth_header_a)
    assert res.status_code == 200 # success

@pytest.mark.asyncio
async def test_note_update(client:AsyncClient, auth_header_a, a_random_note_id) -> None:
    """Test Update Note"""
    
    res = await client.post(f'/v1/note/{a_random_note_id}', headers=auth_header_a, json=update_data)

    assert res.status_code == 200 # success
    assert res.json().get('content') == update_data.get('content')
    assert res.json().get('tags') == update_data.get('tags')

@pytest.mark.asyncio
async def test_note_list_by_tag(client:AsyncClient, auth_header_a) -> None:
    """Test list_by_tag"""
    
    # Test list-by-tag created by A using A
    res = await client.get('/v1/note/tag/boring', headers=auth_header_a)
    
    assert res.status_code == 200 # Get Successful
    assert len(res.json()) == 1 # 1 note from update_data
    assert res.json()[0].get('content') == update_data.get('content')
    assert res.json()[0].get('tags') == update_data.get('tags')

@pytest.mark.asyncio
async def test_list_all_tag(client:AsyncClient, auth_header_a) -> None:
    """Test list_by_tag"""
    
    # Test list-all-tag created by A using A
    res = await client.get('/v1/tags', headers=auth_header_a)
    assert res.status_code == 200 # Get Successful
    assert sorted(res.json()) == sorted(['study','completed','funny','boring'])

@pytest.mark.asyncio
async def test_note_delete(client:AsyncClient, auth_header_a, a_random_note_id) -> None:
    """Test Delete"""
    
     # Test delete by id created by A using A
    res = await client.delete(f"/v1/note/{a_random_note_id}", headers=auth_header_a)
    assert res.status_code == 204
    assert res.text == ''

@pytest.mark.asyncio
async def test_note_delete_all(client:AsyncClient, auth_header_a, auth_header_b) -> None:
    """Test delete all"""

    # Test delete all created by A using A

    ## Create Data From B
    for note in create_data:
        res_b = await client.post('/v1/note/', headers=auth_header_b, json=note)

    res_a = await client.delete(f"/v1/note", headers=auth_header_a)
    assert res_a.status_code == 204 # All data from A are gone
    assert res_a.text == ''

    res_a = await client.get('/v1/note/', headers=auth_header_a)
    assert len(res_a.json()) == 0 # Ensure User A Content all delete

    ## User B Contents are intact
    res_b = await client.get('/v1/note/', headers=auth_header_b)
    assert res_b.status_code == 200
    assert len(res_b.json()) == 5 # Ensure User B Content is intact

    res_b = await client.delete(f"/v1/note", headers=auth_header_b) # Delete User B All Content. Clean up

