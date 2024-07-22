from pydantic import Field
from app.models.db.base_model import CreateUpdateSchema


class Review(CreateUpdateSchema):
    content: str = Field(None)
    rating: float = Field(...)
    book: str = Field(...)
    created_by: str = Field(...)
