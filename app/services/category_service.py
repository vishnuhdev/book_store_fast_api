from typing import List

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.db.category_model import Category
from app.models.pydantics.category_pydantics import CategoryCreate, CategoryResponse, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.category

    async def retrieve_categories(self) -> List[CategoryResponse]:
        result = self.collection.find()
        categories = []
        async for category in result:
            category = self.__replace_id(category)
            categories.append(CategoryResponse(**category))
        return categories

    async def create_category(self, category: CategoryCreate) -> CategoryResponse:
        category_dict = category.dict()
        category = Category(**category_dict)
        result = await self.collection.insert_one(category.dict())
        return await self.retrieve_category(result.inserted_id)

    async def retrieve_category(self, inserted_id: str) -> CategoryResponse:
        category = await self.collection.find_one({'_id': ObjectId(inserted_id)})
        category = self.__replace_id(category)
        return CategoryResponse(**category)

    async def update_category(self, category_id: str, category: CategoryUpdate) -> CategoryResponse:
        is_category = await self.collection.find_one({'_id': ObjectId(category_id)})
        if not is_category:
            raise HTTPException(status_code=404, detail='Invalid Category ID')
        category_dict = category.dict(exclude_unset=True)
        await self.collection.update_one({'_id': ObjectId(category_id)}, {'$set': category_dict})
        return await self.retrieve_category(category_id)

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
