from pydantic import Field
from app.models.pydantics.base_model import CreateSchema, RequestSchema


class UserResponse(CreateSchema):
    email: str = Field(...)
    password: str = Field(...)


class UserCreate(RequestSchema):
    email: str = Field(...)
    password: str = Field(...)
