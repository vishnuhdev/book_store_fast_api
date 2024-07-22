from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_database
from app.services.review_service import ReviewService
from app.models.pydantics.review_pydantics import ReviewResponse, ReviewCreate, ReviewUpdate
from app.utils.JWTToken import JWTBearer

review_routers = APIRouter(
    prefix="/books",
    tags=['Reviews']
)


@review_routers.get(
    '/{book_id}/reviews',
    response_model=List[ReviewResponse]
)
async def retrieve_reviews(
        book_id: str,
        user_id: str = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    service = ReviewService(db)
    return await service.retrieve_reviews(user_id, book_id)


@review_routers.post(
    '/{book_id}/reviews',
    status_code=201,
    response_model=ReviewResponse)
async def create_review(
        review: ReviewCreate,
        book_id: str,
        user_id: str = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = ReviewService(db)
    return await service.create_review(review, book_id, user_id)


@review_routers.get('/{book_id}/reviews/{review_id}',
                    response_model=ReviewResponse)
async def retrieve_review(
        review_id: str,
        book_id: str = None,
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = ReviewService(db)
    return await service.retrieve_review(review_id)


@review_routers.put('/{book_id}/reviews/{review_id}', response_model=ReviewResponse)
async def update_review(
        review_id: str,
        review: ReviewUpdate,
        book_id: str = None,
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = ReviewService(db)
    return await service.update_review(
        review_id,
        review,
    )
