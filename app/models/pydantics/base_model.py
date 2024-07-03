from datetime import datetime
from pydantic import BaseModel, Field


class RequestSchema(BaseModel):
    pass


class CreateSchema(BaseModel):
    id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreateUpdateSchema(BaseModel):
    id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
