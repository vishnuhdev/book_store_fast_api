from typing import List

from app.models.pydantics.base_model import CreateSchema, BaseSchema, RequestSchema
from pydantic import Field


class PublisherResponse(CreateSchema):
    name: str = Field(..., examples=['Penguin Random House'])
    location: str = Field(..., examples=['Chennai, TN, India'])
    books: List[BaseSchema] = Field(..., examples=[BaseSchema(id='6683f946ec61bfa6a3c2d7c7', name='Book name')])


class PublisherCreate(RequestSchema):
    name: str = Field(..., examples=['Penguin Random House'])
    location: str = Field(..., examples=['Chennai, TN, India'])
    books: List[str] = Field(..., examples=[['6683f946ec61bfa6a3c2d7c7', '6683f946ec61bfa6a3c2d7c7']])


class PublisherUpdate(RequestSchema):
    name: str = Field(None, examples=['Penguin Random House'])
    location: str = Field(None, examples=['Chennai, TN, India'])
    books: List[str] = Field(None, examples=[['6683f946ec61bfa6a3c2d7c7', '6683f946ec61bfa6a3c2d7c7']])

