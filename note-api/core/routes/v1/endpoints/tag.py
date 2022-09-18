from typing import List
from fastapi import APIRouter, Depends

from core.config.database import db
from core.utils.authentication import get_current_user
from core.models.user import User

router = APIRouter()

@router.get("/", response_model=List[str])
async def list(current_user: User = Depends(get_current_user)):
    res = await db.notes.distinct("tags", {"owners": current_user.username})
    return res
