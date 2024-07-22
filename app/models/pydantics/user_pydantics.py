from pydantic import Field, EmailStr
from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema


class UserResponse(CreateUpdateSchema):
    name: str = Field(..., examples=["Joseph"])
    email: str = Field(..., examples=["test@gmail.com"])
    gender: str = Field(..., examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(..., examples=[25])


class UserCreate(RequestSchema):
    name: str = Field(..., examples=["Albert Joseph"])
    email: EmailStr = Field(..., examples=["test@gmail.com"])
    password: str = Field(..., examples=["password@123"])
    gender: str = Field(..., examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(..., examples=[25])


class UserLogin(RequestSchema):
    email: EmailStr = Field(..., examples=["test@gmail.com"])
    password: str = Field(..., examples=["password"])


class UserUpdate(RequestSchema):
    name: str = Field(None, examples=["Albert Joseph"])
    gender: str = Field(None, examples=['Male'])
    phone_number: str = Field(None, examples=['+918856852123'])
    age: int = Field(None, examples=[25])


class ChangePasswordRequest(RequestSchema):
    current_password: str = Field(..., examples=["old password"])
    new_password: str = Field(..., examples=["new password"])
