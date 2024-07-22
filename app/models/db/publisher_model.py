from typing import List

from pydantic import Field, BaseModel


class Publisher(BaseModel):
    name: str = Field(...)
    location: str = Field(...)
    books: List[str] = Field(...)

