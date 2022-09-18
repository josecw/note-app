from passlib.hash import pbkdf2_sha256
from typing import List
from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import Response, JSONResponse

from core.models.user import User, UserLogout
from core.utils.authentication import signJWT

router = APIRouter()

exclude_fields = ["id","created_at", "password", "last_logon_dt"]


@router.post("/register", description="Register User")
async def create_user(req: User):
    
    res = await User.find_one(User.username == req.username)

    if res:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
            content={"message": f"User with email {req.username} exists", "username": req.username})
    
    req.password = pbkdf2_sha256.hash(req.password)
    res = await req.save()

    return JSONResponse(status_code=status.HTTP_200_OK,
        content={"message": f"User {req.username} created successfully."})

@router.post("/login", tags=["auth"])
async def login(user: User):

    res = await User.find_one(User.username == user.username)
    if res:
       match = pbkdf2_sha256.verify(user.password, res.password)
       
       if match:
            res.last_logon_dt = datetime.utcnow()
            await res.save()
            return signJWT(user.username)
    
    return JSONResponse(status_code=status.HTTP_200_OK,
        content={"message": f"login failed"})

@router.post("/logout", tags=["auth"])
async def logout(req: UserLogout):
    
    user = await User.find_one(User.username == req.username)
    user.jwt_secret = req.jwt_secret
    await user.save()

    return Response(status_code=status.HTTP_200_OK)

    