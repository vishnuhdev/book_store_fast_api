from pydantic import Field

from app.models.pydantics.base_model import CreateUpdateSchema, RequestSchema


class ReviewResponse(CreateUpdateSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: int = Field(..., examples=[2])
    created_by: str = Field(..., examples=['66829dde942d3b6234dcdbc6c'])
    book_id: str = Field(..., examples=['66829dde942d3b6234dcdbc6c'])


class ReviewCreate(RequestSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: int = Field(..., examples=[2])


class ReviewUpdate(RequestSchema):
    content: str = Field(None, examples=['This is the content'])
    rating: int = Field(None, examples=[2])