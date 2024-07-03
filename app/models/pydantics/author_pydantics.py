from typing import List
from pydantic import Field
from app.models.pydantics.base_model import RequestSchema, CreateUpdateSchema
from app.models.pydantics.book_pydantics import BaseSchema


class CreateAuthor(RequestSchema):
    name: str = Field(..., examples=["James"])
    age: int = Field(..., examples=[25])
    gender: str = Field(..., examples=['Male', 'Female', 'Prefer not to say'])
    awards: List[str] = Field(None, examples=[
        ["Best writer of the decade - 2018 "]
    ])


class UpdateAuthor(RequestSchema):
    name: str = Field(None, examples=["James"])
    age: int = Field(None, examples=[25])
    gender: str = Field(None, examples=['Male', 'Female', 'Prefer not to say'])
    awards: List[str] = Field(None, examples=[
        ["Best writer of the decade - 2018 "]
    ])


class AuthorResponse(CreateUpdateSchema):
    name: str = Field(..., examples=["James"])
    books: List[BaseSchema] = Field(None, examples=[
        [
            BaseSchema(name="Disney Land", id='66829dde942d3b624dcdbc6c'),
            BaseSchema(name="The Island", id='66829dde942d3b6234dcdbc6c'),
            BaseSchema(name="Make in India", id='65454adse942d3b6234dcdbc6c'),
        ]
    ])
    age: int = Field(..., examples=[25])
    gender: str = Field(..., examples=['Male', 'Female', 'Prefer not to say'])
    awards: List[str] = Field(None, examples=[
        "Best writer of the decade - 2018 "
    ])
    total_published: int = Field(None, examples=[5])
