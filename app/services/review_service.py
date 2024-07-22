from typing import List

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.db.review_model import Review
from app.models.pydantics.base_model import BaseSchema
from app.models.pydantics.review_pydantics import ReviewResponse, ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.reviews
        self.user_collection = self.db.users
        self.book_collection = self.db.books

    async def retrieve_reviews(self, user_id: str, book_id: str) -> List[ReviewResponse]:
        result = self.collection.find({'book_id': book_id})
        reviews = []
        async for review in result:
            review = self.__replace_id(review)
            review['created_by'] = await self.__get_user_detail(user_id)
            review['book'] = await self.__get_book(book_id)
            reviews.append(ReviewResponse(**review))
        return reviews

    async def create_review(self, review: ReviewCreate, book_id: str, user_id: str) -> ReviewResponse:
        review_dict = review.dict()
        review_dict['created_by'] = user_id
        review_dict['book'] = book_id
        review = Review(**review_dict)
        inserted = await self.collection.insert_one(review.dict())
        return await self.retrieve_review(str(inserted.inserted_id))

    async def retrieve_review(self, review_id: str) -> ReviewResponse:
        review = await self.collection.find_one({'_id': ObjectId(review_id)})
        review = self.__replace_id(review)
        user_id = review['created_by']
        book_id = review['book']
        review['created_by'] = await self.__get_user_detail(user_id)
        review['book'] = await self.__get_book(book_id)
        return ReviewResponse(**review)

    async def update_review(
            self,
            review_id: str,
            review: ReviewUpdate,
    ) -> ReviewResponse:
        if not await self.collection.find_one({'_id': ObjectId(review_id)}):
            raise HTTPException(status_code=404, detail='Review not found.')
        review_dict = review.dict(exclude_unset=True)
        await self.collection.update_one({'_id': ObjectId(review_id)}, {'$set': review_dict})
        return await self.retrieve_review(review_id)

    async def __get_user_detail(self, user_id: str) -> BaseSchema:
        user = await self.user_collection.find_one({'_id': ObjectId(user_id)})
        user = self.__replace_id(user)
        return BaseSchema(**user)

    async def __get_book(self, book_id: str) -> BaseSchema:
        book = await self.book_collection.find_one({'_id': ObjectId(book_id)})
        book = self.__replace_id(book)
        return BaseSchema(**book)

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
