from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
