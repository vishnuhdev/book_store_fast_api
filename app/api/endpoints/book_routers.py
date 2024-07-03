from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.models.pydantics.book_pydantics import (
    BookCreate,
    BookUpdate,
    BookResponse, CategoryModel, CategoryEnums
)
from app.database import get_database
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.book_service import BookService

book_router = APIRouter(prefix='/books', tags=['Books'])


@book_router.get('/', response_model=List[BookResponse])
async def retrieve_books(
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = BookService(db)
    return await service.retrieve_books()


@book_router.post('/', response_model=BookResponse, status_code=201)
async def create_book(
        book: BookCreate,
        category: str = Query("Fiction", enum=["Fiction", "Non-Fiction", "Comedy", "Rom-Com"]),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = BookService(db)
    return await service.create_book(book, category)


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
        book_id: str, book: BookUpdate, db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = BookService(db)
        return await service.update_book(book_id, book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@book_router.delete('/{book_id}', status_code=204)
async def delete_book(
        book_id: str,
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = BookService(db)
        await service.delete_book(book_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
