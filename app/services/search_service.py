from http import HTTPStatus
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.pydantics.search_pydantics import SearchBooks, BaseIdName, SearchAuthor, SearchCategory, SearchReview, \
    SearchUser


class SearchService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.books = self.db.books
        self.reviews = self.db.reviews
        self.author = self.db.author
        self.publisher = self.db.publishers
        self.category = self.db.category
        self.reviews = self.db.reviews
        self.users = self.db.users

    async def search_books(self, input_str: str) -> List[SearchBooks]:
        query = {
            "$or": [
                {"name": {"$regex": input_str, "$options": "i"}},
                {"description": {"$regex": input_str, "$options": "i"}},
                {"author": {"$regex": input_str, "$options": "i"}},
                {"category.name": {"$regex": input_str, "$options": "i"}},
            ]
        }

        cursor = self.books.find(query)
        books = []
        async for document in cursor:
            result = self.__replace_id(document)
            result['author'] = await self.__get_author(result['author'])
            result['category'] = await self.__get_category_detail(result['category']['name'])
            publisher = await self.__get_publisher(result['id'])
            if publisher is not None:
                result['publisher'] = publisher
            review = await self.__get_review_detail(result['id'])
            result['average_rating'] = review['avg_rating']
            result['total_reviews'] = review['total_reviews']
            books.append(SearchBooks(**result))

        return books

    async def search_author(self, input_str) -> List[SearchAuthor]:
        query = {
            "$or": [
                {"name": {"$regex": input_str, "$options": "i"}},
                {"age": {"$regex": input_str, "$options": "i"}},
                {"awards": {"$regex": input_str, "$options": "i"}},
                {"gender": {"$regex": input_str, "$options": "i"}},
            ]
        }

        cursor = self.author.find(query)
        authors = []
        async for document in cursor:
            result = self.__replace_id(document)
            books = await self.get_book_details(result['id'])
            result['latest_books'] = books[0:1]
            result['total_published'] = len(books)
            authors.append(SearchAuthor(**result))
        return authors

    async def search_category(self, input_str) -> List[SearchCategory]:
        query = {
            "$or": [
                {"name": {"$regex": input_str, "$options": "i"}},
                {"description": {"$regex": input_str, "$options": "i"}},
            ]
        }

        cursor = self.category.find(query)
        category = []
        async for document in cursor:
            result = self.__replace_id(document)
            category.append(SearchCategory(**result))
        return category

    async def search_reviews(self, input_str) -> List[SearchReview]:
        query = {
            "$or": [
                {"content": {"$regex": input_str, "$options": "i"}},
                {"rating": {"$regex": input_str, "$options": "i"}},
                {"book": {"$regex": input_str, "$options": "i"}},
                {"created_by": {"$regex": input_str, "$options": "i"}},
            ]
        }

        cursor = self.reviews.find(query)
        reviews = []
        async for document in cursor:
            result = self.__replace_id(document)
            user_id = result['created_by']
            book_id = result['book']
            result['created_by'] = await self.__get_user_detail(user_id)
            result['book'] = await self.__get_book(book_id)
            reviews.append(SearchReview(**result))
        return reviews

    async def search_user(self, input_str) -> List[SearchUser]:
        query = {
            "$or": [
                {"name": {"$regex": input_str, "$options": "i"}},
                {"email": {"$regex": input_str, "$options": "i"}},
                {"gender": {"$regex": input_str, "$options": "i"}},
                {"phone_number": {"$regex": input_str, "$options": "i"}},
                {"age": {"$regex": input_str, "$options": "i"}},
            ]
        }

        cursor = self.users.find(query)
        reviews = []
        async for document in cursor:
            result = self.__replace_id(document)
            reviews.append(SearchUser(**result))
        return reviews

    async def get_book_details(self, author_id: str):
        result = self.books.find({'author': author_id})
        total_books = []
        async for book in result:
            book = self.__replace_id(book)
            book = BaseIdName(**book)
            total_books.append(book)
        return total_books

    async def __get_author(self, author_id: str) -> BaseIdName:
        author = await self.author.find_one({'_id': ObjectId(author_id)})
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Author not found'
            )
        author = self.__replace_id(author)
        return BaseIdName(**author)

    async def __get_publisher(self, book_id: str):
        publisher = await self.publisher.find_one({'books': book_id})
        if not publisher:
            return None
        publisher = self.__replace_id(publisher)
        return publisher

    async def __get_category_detail(self, category) -> BaseIdName:
        category = await self.category.find_one({'name': category})
        if not category:
            raise HTTPException(
                status_code=404,
                detail='Category not found.'
            )
        category = self.__replace_id(category)
        return BaseIdName(**category)

    async def __get_user_detail(self, user_id: str) -> BaseIdName:
        user = await self.users.find_one({'_id': ObjectId(user_id)})
        user = self.__replace_id(user)
        return BaseIdName(**user)

    async def __get_book(self, book_id: str) -> BaseIdName:
        book = await self.books.find_one({'_id': ObjectId(book_id)})
        book = self.__replace_id(book)
        return BaseIdName(**book)

    @staticmethod
    async def __get_review_detail(self, book_id: str) -> dict[str, int | float]:
        total_reviews_count = 0
        total_ratings = 0
        review_cursor = self.reviews.find({'book_id': book_id})

        async for review in review_cursor:
            rating = review['rating']
            total_ratings += rating
            total_reviews_count += 1

        avg_rating = round(total_ratings / total_reviews_count, 2) if total_reviews_count > 0 else 0

        return {
            'avg_rating': avg_rating,
            'total_reviews': total_reviews_count,
        }

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
