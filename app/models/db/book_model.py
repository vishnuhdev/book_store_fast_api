from app.models.db.base_model import CreateUpdateSchema
from pydantic import Field
from app.models.pydantics.category_pydantics import CategoryResponse


class Book(CreateUpdateSchema):
    name: str = Field(...)
    description: str = Field(None)
    author: str = Field(...)
    is_published: bool = Field(False)
    category: CategoryResponse = Field(...)

