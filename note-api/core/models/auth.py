from pydantic import Field
from typing import Union
from pydantic_aioredis import Model
import time

from core.config import settings


class TokenData(Model):
    _primary_key_field: str = "username"
    username: Union[str, None] = None
    expired_dt: float = Field(default=time.time() + settings.JWT_EXPIRY)
