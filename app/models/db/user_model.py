from app.models.db.base_model import CreateUpdateSchema
from pydantic import Field


class User(CreateUpdateSchema):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    gender: str = Field(...)
    phone_number: str = Field(None)
    age: int = Field(...)
