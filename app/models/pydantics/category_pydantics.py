from pydantic import Field

from app.models.pydantics.base_model import CreateSchema, RequestSchema


class CategoryResponse(CreateSchema):
    name: str = Field(...)
    description: str = Field(...)


class CategoryCreate(RequestSchema):
    name: str = Field(..., examples=['Fiction'])
    description: str = Field(..., examples=['Fiction description'])


class CategoryUpdate(RequestSchema):
    name: str = Field(None, examples=['Fiction'])
    description: str = Field(None, examples=['Fiction description'])
