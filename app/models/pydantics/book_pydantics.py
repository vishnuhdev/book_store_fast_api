from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic.dataclasses import dataclass

from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema, BaseSchema
from pydantic import Field, BaseModel


class CategoryEnums(str, Enum):
    FICTION = "FICTION"
    NON_FICTION = "NON-FICTION"
    BIOGRAPHY = "BIOGRAPHY"
    AUTOBIOGRAPHY = "AUTOBIOGRAPHY"
    SCIENCE_FICTION = "SCIENCE FICTION"
    FANTASY = "FANTASY"
    MYSTERY = "MYSTERY"
    THRILLER = "THRILLER"
    ROMANCE = "ROMANCE"
    HISTORICAL_FICTION = "HISTORICAL FICTION"
    SELF_HELP = "SELF-HELP"
    BUSINESS = "BUSINESS"
    HISTORY = "HISTORY"
    SCIENCE = "SCIENCE"
    TRAVEL = "TRAVEL"
    COOKBOOK = "COOKBOOK"
    ART_PHOTOGRAPHY = "ART & PHOTOGRAPHY"
    RELIGION_SPIRITUALITY = "RELIGION & SPIRITUALITY"
    PHILOSOPHY = "PHILOSOPHY"
    CHILDREN_BOOKS = "CHILDREN'S BOOKS"


@dataclass
class CategoryModel:
    category: list[CategoryEnums] = Query(...)


class Category(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(None, examples=['This is description'])


class BookCreate(RequestSchema):
    name: str = Field(..., examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: str = Field(None, examples=['This is description about a book.'])
    category: str = Field(..., examples=['FICTION'])


class BookUpdate(RequestSchema):
    name: Optional[str] = Field(None, examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: Optional[str] = Field(None, examples=['This is description about a book.'])
    is_published: Optional[bool] = Field(False)


class BookResponse(CreateUpdateSchema):
    name: str = Field(None, examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: str = Field(None, examples=['This is description about a book.'])
    author: BaseSchema = Field(None, examples=[BaseSchema(id='65454adse942d3b6234dcdbc6c', name='James')])
    is_published: bool = Field(False)
    category: BaseSchema = Field(...)
    publisher: BaseSchema = Field(None)
    average_rating: float = Field(..., examples=[4.6])
    total_reviews: int = Field(..., examples=[120])


class BookCreateResponse(CreateUpdateSchema):
    name: str = Field(None, examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: str = Field(None, examples=['This is description about a book.'])
    author: BaseSchema = Field(None, examples=[BaseSchema(id='65454adse942d3b6234dcdbc6c', name='James')])
    is_published: bool = Field(False)
    category: BaseSchema = Field(...)
