from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from core.utils.generator import gen_id
from beanie import Document


class Note(Document):

    id: int = Field(default_factory=gen_id, title="id")
    content: str
    tags: list[str] = []
    owners: list[EmailStr] = Field(default=[], alias="owners")
    created_dt: datetime = Field(alias="created_dt")
    updated_dt: datetime= Field(alias="updated_dt")

    class Settings:
        name = "notes"

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": 553364,
                "content": "Don't forget to upload screenshots",
                "tags": [
                    "work",
                    "project-1"
                ]
            }
        }

class NoteRead(Note):

    id: int 
    content: str
    tags: list[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": 553364,
                "content": "Don't forget to upload screenshots",
                "tags": [
                    "work",
                    "project-1"
                ]
            }
        }


class NoteCreate(BaseModel):

    content: str
    tags: list[str] = []
    owners: list[int] = Field(default=[], alias="owners")
    created_dt: datetime = Field(default_factory=datetime.utcnow, alias="created_dt")
    updated_dt: datetime = Field(default_factory=datetime.utcnow, alias="updated_dt")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": "Don't forget to upload screenshots",
                "tags": [
                    "work", "project-1"
                ]

            }
        }


class NoteUpdate(BaseModel):

    content: str
    tags: list[str] = []
    updated_dt: datetime = Field(default_factory=datetime.utcnow, alias="updated_dt")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": "Don't forget to upload screenshots",
                "tags": [
                    "work", "project-1"
                ]

            }
        }