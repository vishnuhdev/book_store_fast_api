from pydantic import Field
from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema


class UserResponse(CreateUpdateSchema):
    name: str = Field(..., examples=["Joseph"])
    email: str = Field(..., examples=["test@gamil.com"])
    gender: str = Field(..., examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(..., examples=[25])


class UserCreate(RequestSchema):
    name: str = Field(..., examples=["Albert Joseph"])
    email: str = Field(..., examples=["test@gamil.com"])
    password: str = Field(..., examples=["password@123"])
    gender: str = Field(..., examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(..., examples=[25])


class UserUpdate(RequestSchema):
    name: str = Field(None, examples=["Albert Joseph"])
    email: str = Field(None, examples=["test@gamil.com"])
    gender: str = Field(None, examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(None, examples=[25])
