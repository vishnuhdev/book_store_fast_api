from datetime import datetime
from pydantic import BaseModel, Field


class CreateSchema(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CreateUpdateSchema(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
