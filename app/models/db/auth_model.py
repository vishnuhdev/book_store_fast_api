from pydantic import Field

from app.models.db.base_model import CreateSchema


class User(CreateSchema):
    email: str = Field(...)
    password: str = Field(...)
