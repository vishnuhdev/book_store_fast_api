from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient

from app.database import get_database
from app.models.pydantics.base_model import TokenPayload
from app.models.pydantics.book_pydantics import (
    BookCreate,
    BookUpdate,
    BookResponse,
)
from app.services.book_service import BookService
from app.utils.JWTToken import JWTBearer

book_router = APIRouter(prefix='/books', tags=['Books'])


@book_router.get('/', response_model=List[BookResponse])
async def retrieve_all_books(
        publish_category: str = Query("None", enum=['None', 'Published', 'Non-Published']),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = BookService(db)
    return await service.retrieve_books(publish_category)


@book_router.post('/', response_model=BookResponse, status_code=201)
async def create_book(
        book: BookCreate,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = BookService(db)
    return await service.create_book(book, user)


@book_router.post('/{book_id}/publish', response_model=BookResponse, status_code=201)
async def publish_book(
        book_id: str,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = BookService(db)
    return await service.publish_book(book_id, user)


@book_router.get('/{book_id}', response_model=BookResponse)
async def retrieve_book(
        book_id: str, db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = BookService(db)
        return await service.retrieve_book(book_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@book_router.put('/{book_id}', response_model=BookResponse)
async def update_book(
        book_id: str,
        book: BookUpdate,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = BookService(db)
        return await service.update_book(book_id, book, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@book_router.delete('/{book_id}', status_code=204)
async def delete_book(
        book_id: str,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = BookService(db)
        await service.delete_book(book_id, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
