from typing import List

from pydantic import BaseModel, Field


class IdModel(BaseModel):
    id: str = Field(..., examples=['6683f946ec61bfa6a3c2d7c7'])


class BaseIdName(BaseModel):
    id: str = Field(..., examples=["6683e1a4710824df4e5d76e9"])
    name: str = Field(..., examples=["name"])


class SearchBooks(BaseIdName):
    author: BaseIdName = Field(...)
    category: BaseIdName = Field(...)
    publisher: BaseIdName = Field(None,)
    average_rating: float = Field(...)
    total_reviews: int = Field(...)


class SearchAuthor(BaseIdName):
    age: int = Field(..., examples=[25])
    gender: str = Field(..., examples=['Male'])
    awards: List[str] = Field(..., examples=['Best writer of the decade - 2018 "'])
    latest_books: List[BaseIdName] = Field(None)
    total_published: int = Field(..., examples=[69])


class SearchReview(IdModel):
    content: str = Field(..., examples=['Great review!'])
    rating: float = Field(..., examples=[4.5])
    created_by: BaseIdName = Field(...)
    book: BaseIdName = Field(...)


class SearchUser(BaseIdName):
    email: str = Field(..., examples=['test@gmail.com'])
    gender: str = Field(..., examples=['Male'])
    phone_number: str = Field(..., examples=['+918856852123'])
    age: int = Field(..., examples=[25])


class SearchCategory(BaseIdName):
    description: str = Field(..., examples=['Fiction description'])


class SearchByBooks(BaseModel):
    result: List[SearchBooks] = Field(...)


class SearchByAuthors(BaseModel):
    result: List[SearchAuthor] = Field(...)


class SearchByCategories(BaseModel):
    result: List[SearchCategory] = Field(...)


class SearchByReviews(BaseModel):
    result: List[SearchReview] = Field(...)


class SearchByUsers(BaseModel):
    result: List[SearchUser] = Field(...)
