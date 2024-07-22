from pydantic import Field, EmailStr

from app.models.db.base_model import CreateSchema


class User(CreateSchema):
    email: EmailStr = Field(...)
    password: str = Field(...)
