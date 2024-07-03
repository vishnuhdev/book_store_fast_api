from typing import List

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.db.review_model import Review
from app.models.pydantics.review_pydantics import ReviewResponse, ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.reviews

    async def retrieve_reviews(self, user_id: str, book_id: str) -> List[ReviewResponse]:
        result = self.collection.find({'book_id': book_id})
        reviews = []
        async for review in result:
            review = self.__replace_id(review)
            review['created_by'] = user_id
            review['book_id'] = book_id
            reviews.append(ReviewResponse(**review))
        return reviews

    async def create_review(self, review: ReviewCreate, book_id: str, user_id: str) -> ReviewResponse:
        review_dict = review.dict()
        review_dict['created_by'] = user_id
        review_dict['book_id'] = book_id
        review = Review(**review_dict)
        inserted = await self.collection.insert_one(review.dict())
        return await self.retrieve_review(str(inserted.inserted_id))

    async def retrieve_review(self, review_id: str) -> ReviewResponse:
        review = await self.collection.find_one({'_id': ObjectId(review_id)})
        review = self.__replace_id(review)
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

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
