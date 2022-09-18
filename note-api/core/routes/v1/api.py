from fastapi import APIRouter

from core.routes.v1.endpoints import note, tag, user, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(note.router, prefix="/note", tags=["notes"])
api_router.include_router(tag.router, prefix="/tags", tags=["tags"])
api_router.include_router(user.router, prefix="/user", tags=["users"])