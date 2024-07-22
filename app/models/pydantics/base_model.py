from datetime import datetime
from pydantic import BaseModel, Field


class RequestSchema(BaseModel):
    pass


class BaseSchema(BaseModel):
    id: str = Field(..., examples=['6683f946ec61bfa6a3c2d7c7'])
    name: str = Field(..., examples=["Harry Porter Chambers of secrets (VOLUME 1)"])


class CreateSchema(BaseModel):
    id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreateUpdateSchema(BaseModel):
    id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TokenRequest(BaseModel):
    id: str
    email: str


class TokenPayload(BaseModel):
    exp: int = None
    email: str = None
    id: str = None
    token_type: str = None


class TokenResponse(BaseModel):
    access_token: str = Field(..., examples=["eyJQGdtYWlsLmNvbSIsImlkIjoiNzBjMzhkYTEtNmEzYS00NDQ2LTg5MGMtNDYzOTM4YzA0NmFhIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiJ9.IJI-K-BsqODkgjI8MN-NBxBKmIxQ6z_ZOLhmKWMouTc"])
    refresh_token: str = Field(..., examples=["eyJQGdtYWlsLmNvbSIsImlkIjoiNzBjMzhkYTEtNmEzYS00NDQ2LTg5MGMtNDYzOTM4YzA0NmFhIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiJ9.IJI-K-BsqODkgjI8MN-NBxBKmIxQ6z_ZOLhmKWMouTc"])
