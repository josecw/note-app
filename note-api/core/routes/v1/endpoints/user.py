from passlib.hash import pbkdf2_sha256
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException
from fastapi.responses import Response, JSONResponse

from core.models.user import User
from core.utils.authentication import signJWT, JWTBearer, get_current_user

router = APIRouter()

exclude_fields = ["id", "created_dt", "password", "jwt_secret"]

@router.get("/current_user", response_model=User, response_model_exclude=exclude_fields)
async def current_user(current_user: User = Depends(get_current_user)):
    return current_user

