from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

from core.utils.generator import gen_jwt_secret

class User(Document):

    username: Indexed(EmailStr, unique=True) = Field(..., description="User name in email format")
    password: str = Field(...)
    created_dt: datetime = Field(default_factory=datetime.utcnow, alias="created_dt")
    last_logon_dt: Optional[datetime]
    jwt_secret: str = Field(default_factory=gen_jwt_secret)

    class Settings:
        name = "users"
        use_revision = False

    class Config:
        schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "weakpassword"
            }
        }

class UserLogout(BaseModel):

    username: EmailStr
    jwt_secret: str = Field(default_factory=gen_jwt_secret)

    class Settings:
        name = "users"
        use_revision = False

    class Config:
        schema_extra = {
            "example": {
                "username": "user@example.com"
            }
        }