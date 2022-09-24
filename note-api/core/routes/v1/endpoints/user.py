from fastapi import APIRouter, Depends

from core.models.user import User
from core.utils.authentication import get_current_user

router = APIRouter()

exclude_fields = ["id", "created_dt", "password", "jwt_secret"]

@router.get("/current_user", response_model=User, response_model_exclude=exclude_fields)
async def current_user(current_user: User = Depends(get_current_user)):
    return current_user

