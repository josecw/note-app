from typing import List
import re

from fastapi import APIRouter, status, Depends
from fastapi.responses import Response, JSONResponse
from beanie.operators import RegEx

from core.models.note import Note, NoteUpdate, NoteCreate
from core.models.user import User
from core.utils.authentication import get_current_user
router = APIRouter()

exclude_fields = ["owners","created_dt","updated_dt"]

# retrieve
@router.get("/", 
    response_model=List[Note], 
    response_model_exclude=exclude_fields)
async def list(current_user: User = Depends(get_current_user)):
    notes = await Note.find(Note.owners == current_user.username).to_list()
    return notes


@router.get("/{id}", 
    response_model=Note,
    response_model_exclude=exclude_fields)
async def retrieve(id: int, current_user: User = Depends(get_current_user)) :
    if (note := await Note.find_one(Note.id == id, Note.owners == current_user.username)) is not None:
        return note

    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Note {id} is not found", "id": id})

# post
@router.post("/", 
    response_description="Note created successfully",
    response_model=Note,
    response_model_exclude=exclude_fields)
async def create(req: NoteCreate, current_user: User = Depends(get_current_user)):
    #note = jsonable_encoder(note_in)
    
    note = Note(**req.dict()) # Serialize to DB format
    note.owners.append(current_user.username)
    res = await note.create() # Insert
   
    return res

# update
@router.post("/{id}", 
    response_model=Note,
    response_model_exclude=exclude_fields)
async def update(id: int, req: NoteUpdate, current_user: User = Depends(get_current_user)):

    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}

    note = await Note.find_one(Note.id == id, Note.owners == current_user.username)
    if not note:    
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Note {id} is not found", "id": id})

    await note.update(update_query)
    return note
        

# delete
@router.delete("/{id}")
async def delete(id: int, current_user: User = Depends(get_current_user)):

    note = await Note.find_one(Note.id == id, Note.owners == current_user.username)
    if not note:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"Note {id} is not found", "id": id})

    await note.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
# list by Tag
@router.get("/tag/{tag}",  
        response_description="Get all the notes with the same tag a user can access", 
        response_model=List[Note],
        response_model_exclude=exclude_fields)
async def list_by_tag(tag: str, current_user: User = Depends(get_current_user)):
    res = await Note.find(RegEx(Note.tags, tag, 'i'), Note.owners == current_user.username).to_list()
    return res
