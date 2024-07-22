from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models.pydantics.author_pydantics import AuthorResponse, CreateAuthor
from app.models.db.author_model import Author
from fastapi import HTTPException

from app.models.pydantics.book_pydantics import BaseSchema


class AuthorService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.author
        self.book_collection = self.db.books

    async def retrieve_authors(self) -> List[AuthorResponse]:
        result = self.collection.find()
        authors = []
        async for author in result:
            author = self.__replace_id(author)
            books = await self.get_book_details(author['id'])
            author['books'] = books[0:3]
            author['total_published'] = len(books)
            authors.append(AuthorResponse(**author))
        return authors

    async def create_author(self, authRequest: CreateAuthor) -> AuthorResponse:
        author_dict = authRequest.dict()
        author = Author(**author_dict)
        inserted = await self.collection.insert_one(author.dict())
        return await self.retrieve_author(str(inserted.inserted_id))

    async def retrieve_author(self, author_id: str) -> AuthorResponse:
        author = await self.collection.find_one({'_id': ObjectId(author_id)})
        books = await self.get_book_details(author_id)
        author['books'] = books[0:3]
        author['total_published'] = len(books)
        author = self.__replace_id(author)
        return AuthorResponse(**author)

    async def get_book_details(self, author_id: str):
        result = self.book_collection.find({'author': author_id})
        total_books = []
        async for book in result:
            book = self.__replace_id(book)
            book = BaseSchema(**book)
            total_books.append(book)
        return total_books

    async def update_author(self, author_id, author):
        if not await self.collection.find_one({'_id': ObjectId(author_id)}):
            raise HTTPException(status_code=404, detail='Author not found.')
        author_dict = author.dict(exclude_unset=True)
        result = await self.collection.update_one({'_id': ObjectId(author_id)}, {'$set': author_dict})
        return await self.retrieve_author(author_id)

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
