from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from app.models.db.publisher_model import Publisher
from app.models.pydantics.base_model import BaseSchema
from app.models.pydantics.publisher_pydantics import PublisherResponse, PublisherCreate, PublisherUpdate
from bson import ObjectId


class PublisherService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.publishers
        self.book_collection = self.db.books

    async def retrieve_publishers(self) -> List[PublisherResponse]:
        result = self.collection.find()
        publisher_list = []
        async for item in result:
            publisher = self.__replace_id(item)
            books = await self.__get_books(publisher['books'])
            publisher['books'] = books
            publisher_list.append(PublisherResponse(**publisher))
        return publisher_list

    async def create_publisher(self, publisher: PublisherCreate) -> PublisherResponse:
        publisher_dict = publisher.dict()
        publisher = Publisher(**publisher_dict)
        for value in publisher.books:
            if await self.book_collection.find_one({'_id': ObjectId(value)}) is not None:
                await self.book_collection.update_one({'_id': ObjectId(value)}, {'$set': {'is_published': True}})
        result = await self.collection.insert_one(publisher.dict())
        return await self.retrieve_publisher(result.inserted_id)

    async def retrieve_publisher(self, publisher_id: str) -> PublisherResponse:
        publisher = await self.collection.find_one({'_id': ObjectId(publisher_id)})
        books = await self.__get_books(publisher['books'])
        publisher = self.__replace_id(publisher)
        publisher['books'] = books
        return PublisherResponse(**publisher)

    async def update_publisher(self, publisher_id: str, publisher: PublisherUpdate) -> PublisherResponse:
        if not await self.collection.find_one({'_id': ObjectId(publisher_id)}):
            raise HTTPException(status_code=404, detail='Invalid Category ID')
        publisher_dict = publisher.dict(exclude_unset=True)
        await self.collection.update_one({'_id': ObjectId(publisher_id)}, {'$set': publisher_dict})
        return await self.retrieve_publisher(publisher_id)

    async def __get_books(self, book_ids: List[str]) -> List[BaseSchema]:
        total_books = []
        for book_id in book_ids:
            book_details = await self.book_collection.find_one({'_id': ObjectId(book_id)})
            if not book_details:
                print(f"No book found with ID: {book_id}")
                continue
            book = self.__replace_id(book_details)
            try:
                book = BaseSchema(**book)
                total_books.append(book)
            except Exception as e:
                print(f"__get_books_error: {e}")
        return total_books

    @staticmethod
    def __replace_id(publisher):
        publisher['id'] = str(publisher.pop('_id'))
        return publisher
