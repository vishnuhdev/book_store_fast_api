from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models.db.book_model import Book
from app.models.pydantics.book_pydantics import (
    BookCreate,
    BookUpdate,
    BookResponse, BaseSchema
)
from fastapi import HTTPException

from app.models.pydantics.category_pydantics import CategoryResponse


class BookService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.books
        self.category_collection = self.db.category
        self.author_collection = self.db.author

    async def retrieve_books(self) -> List[BookResponse]:
        result = self.collection.find()
        books = []
        async for book in result:
            book = self.__replace_id(book)
            book['custom_variable'] = 'custom_value'
            books.append(BookResponse(**book))
        return books

    async def create_book(self, book: BookCreate, category: str) -> BookResponse:
        book_dict = book.dict()
        book_dict['category'] = await self.__get_category_detail(category)
        book = Book(**book_dict)
        inserted = await self.collection.insert_one(book.dict())
        return await self.retrieve_book(str(inserted.inserted_id), book.author)

    async def retrieve_book(self, book_id: str, author_id: str) -> BookResponse:
        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        book = self.__replace_id(book)
        book['custom_variable'] = 'custom_value'
        book['author'] = await self.__get_author(author_id)
        return BookResponse(**book)

    async def update_book(self, book_id: str, book: BookUpdate) -> BookResponse:
        if not await self.collection.find_one({'_id': ObjectId(book_id)}):
            raise HTTPException(status_code=404, detail='Book not found.')
        book_dict = book.dict(exclude_unset=True)
        result = await self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': book_dict})
        return await self.retrieve_book(book_id, result['author'])

    async def delete_book(self, book_id: str) -> None:
        if not await self.collection.find_one({'_id': ObjectId(book_id)}):
            raise HTTPException(status_code=404, detail='Book not found.')
        await self.collection.delete_one({'_id': ObjectId(book_id)})

    async def __get_category_detail(self, category) -> CategoryResponse:
        category = await self.category_collection.find_one({'name': category})
        category = self.__replace_id(category)
        return CategoryResponse(**category)

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document

    async def __get_author(self, author_id: str) -> BaseSchema:
        author = await self.author_collection.find_one({'_id': ObjectId(author_id)})
        author = self.__replace_id(author)
        return BaseSchema(**author)


