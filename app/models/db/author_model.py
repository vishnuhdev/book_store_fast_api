from typing import List
from pydantic import Field
from app.models.db.base_model import CreateSchema


class Author(CreateSchema):
    name: str = Field(...)
    age: int = Field(None)
    awards: List[str] = Field(None)
    gender: str = Field(...)

