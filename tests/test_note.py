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

@pytest.mark.asyncio
async def test_note_crud_a(client:AsyncClient, auth_payload_a, auth_payload_b) -> None:
    """Test CRUD on user a"""

    db.notes.drop()

    headers_a = {"AUTHORIZATION": f"Bearer {auth_payload_a.get('token')}"}
    headers_b = {"AUTHORIZATION": f"Bearer {auth_payload_b.get('token')}"}
    
    f_create = open('tests/data/create_data.json')
    create_data = json.load(f_create)

    f_update = open('tests/data/update_data.json')
    update_data = json.load(f_update)
    
    # Test Create
    for note in create_data:
        res_a_ins = await client.post('/v1/note/', headers=headers_a, json=note)
        assert res_a_ins.status_code == 200
        assert res_a_ins.json().get('content') == note.get('content')
        assert res_a_ins.json().get('tags') == note.get('tags')

    # Test List data created by A
    res_a_list = await client.get('/v1/note/', headers=headers_a)
    
    assert res_a_list.status_code == 200
    assert isinstance(res_a_list.json(), list)
    for i in res_a_list.json(): assert isinstance(i, dict)
    assert len(res_a_list.json()) == len(create_data)

    # Test List data created by A using B
    res_b_list = await client.get('/v1/note/', headers=headers_b)

    assert res_b_list.status_code == 200
    assert len(res_b_list.json()) == 0

    # Test get data created by A using B
    id = res_a_list.json()[-1].get('_id')
    res_b_get = await client.get(f'/v1/note/{id}', headers=headers_b)

    assert res_b_get.status_code == 404 # No access
    
    # Test update data created by A using B
    id = res_a_list.json()[-1].get('_id')
    res_b_get = await client.post(f'/v1/note/{id}', headers=headers_b, json=update_data)

    assert res_b_get.status_code == 404 # No access

    # Test delete data created by A using B
    id = res_a_list.json()[-1].get('_id')
    res_b_get = await client.delete(f'/v1/note/{id}', headers=headers_b)

    assert res_b_get.status_code == 404 # No access

    # Test list-by-tag created by A using B
    res_b_tag = res_a_list.json()[-1].get('tags')[0]
    res_b_get = await client.get(f'/v1/note/tag/{res_b_tag}', headers=headers_b)
    
    assert res_b_get.status_code == 200 # Get Successful
    assert len(res_b_get.json()) == 0 # But Empty

    # Test list-all-tag using B
    res_b_all_tag = await client.get(f'/v1/tags/', headers=headers_b)
    assert res_b_all_tag.status_code == 200 # Get Successful
    assert len(res_b_all_tag.json()) == 0 # But Empty

    # Test get data created by A using A
    id = res_a_list.json()[-1].get('_id')
    res_a_get = await client.get(f'/v1/note/{id}', headers=headers_a)
    assert res_a_get.status_code == 200 # success

    # Test update data created by A using A
    id = res_a_list.json()[-1].get('_id')
    res_a_upd = await client.post(f'/v1/note/{id}', headers=headers_a, json=update_data)

    assert res_a_upd.status_code == 200 # success
    assert res_a_upd.json().get('content') == update_data.get('content')
    assert res_a_upd.json().get('tags') == update_data.get('tags')

    # Test list-by-tag created by A using A
    res_a_get = await client.get('/v1/note/tag/boring', headers=headers_a)
    
    assert res_a_get.status_code == 200 # Get Successful
    assert len(res_a_get.json()) == 1 # 1 note from update_data
    assert res_a_get.json()[0].get('content') == update_data.get('content')
    assert res_a_get.json()[0].get('tags') == update_data.get('tags')

    # Test list-all-tag created by A using A
    res_a_all_tag = await client.get('/v1/tags', headers=headers_a)
    assert res_a_all_tag.status_code == 200 # Get Successful
    assert sorted(res_a_all_tag.json()) == sorted(['study','completed','funny','boring'])


    # Test delete by id created by A using A
    res_a_del = await client.delete(f"/v1/note/{id}", headers=headers_a)
    assert res_a_del.status_code == 204
    assert res_a_del.text == ''


    # Test delete all created by A using A

    ## Test Create using B
    for note in create_data:
        res_b_ins = await client.post('/v1/note/', headers=headers_b, json=note)

    res_a_del = await client.delete(f"/v1/note", headers=headers_a)
    assert res_a_del.status_code == 204
    assert res_a_del.text == ''

    res_a_list = await client.get('/v1/note/', headers=headers_a)
    assert len(res_a_list.json()) == 0 # Ensure User A Content all delete

    res_b_list = await client.get('/v1/note/', headers=headers_b)
    assert res_b_list.status_code == 200
    assert len(res_b_list.json()) == 5 # Ensure User B Content is intact

    res_b_del = await client.delete(f"/v1/note", headers=headers_b) # Delete User B All Content. Clean up

