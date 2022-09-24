
from typing import List
from datetime import datetime
import time

from fastapi import APIRouter, status
from fastapi.responses import Response, JSONResponse

from core.models.user import User, UserLogout
from core.models.auth import TokenData
from core.utils.authentication import signJWT
from core.utils import password

router = APIRouter()

exclude_fields = ["id","created_at", "password", "last_logon_dt"]


@router.post("/register", description="Register User")
async def create_user(req: User):
    
    res = await User.find_one(User.username == req.username)

    if res:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
            content={"message": f"User with email {req.username} exists", "username": req.username})
    
    req.password = password.hash(req.password)
    res = await req.save()

    return JSONResponse(status_code=status.HTTP_200_OK,
        content={"message": f"User {req.username} created successfully."})

@router.post("/login", tags=["auth"])
async def login(user: User):

    res = await User.find_one(User.username == user.username)
    if res:
       match = password.verify(user.password, res.password)
       
       if match:
            res.last_logon_dt = datetime.utcnow()
            await res.save()
            tokenData = TokenData(username= user.username)
            await TokenData.insert(tokenData)
            return signJWT(tokenData)
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"login failed"})

@router.post("/logout", tags=["auth"])
async def logout(req: UserLogout):
    
    await TokenData.delete(ids=[req.username])

    return Response(status_code=status.HTTP_200_OK)

    