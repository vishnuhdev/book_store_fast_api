from enum import Enum
from typing import List

from fastapi import Query
from pydantic.dataclasses import dataclass

from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema
from pydantic import Field, BaseModel

from app.models.pydantics.category_pydantics import CategoryResponse


class BaseSchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)


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
    author: str = Field(..., examples=['65454adse942d3b6234dcdbc6c'])
    is_published: bool = Field(False)


class BookUpdate(RequestSchema):
    name: str = Field(None, examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: str = Field(None, examples=['This is description about a book.'])
    author: str = Field(None, examples=['65454adse942d3b6234dcdbc6c'])
    is_published: bool = Field(False)


class BookResponse(CreateUpdateSchema):
    name: str = Field(None, examples=['Harry Porter Chambers of secrets (VOLUME 1)'])
    description: str = Field(None, examples=['This is description about a book.'])
    author: BaseSchema = Field(None, examples=[BaseSchema(id='65454adse942d3b6234dcdbc6c', name='James')])
    is_published: bool = Field(False)
    custom_variable: str = Field(...)
    category: CategoryResponse = Field(...)
