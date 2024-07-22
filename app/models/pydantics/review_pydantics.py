from pydantic import Field

from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema, BaseSchema


class ReviewResponse(CreateUpdateSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: float = Field(..., examples=[2])
    created_by: BaseSchema = Field(...)
    book: BaseSchema = Field(...)


class ReviewCreate(RequestSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: float = Field(..., examples=[2])


class ReviewUpdate(RequestSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: float = Field(None, examples=[2])
