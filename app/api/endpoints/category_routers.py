from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.database import get_database
from app.models.pydantics.category_pydantics import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

category_router = APIRouter(prefix='/category', tags=['Category'])


@category_router.get('/', response_model=List[CategoryResponse])
async def retrieve_categories(db: AsyncIOMotorClient = Depends(get_database)):
    service = CategoryService(db)
    return await service.retrieve_categories()


@category_router.post('/', response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncIOMotorClient = Depends(get_database)):
    service = CategoryService(db)
    return await service.create_category(category)


@category_router.get('/{category_id}', response_model=CategoryResponse)
async def retrieve_category(category_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    service = CategoryService(db)
    return await service.retrieve_category(category_id)


@category_router.put('/{category_id}', response_model=CategoryResponse)
async def update_category(category_id: str, category: CategoryUpdate, db: AsyncIOMotorClient = Depends(get_database)):
    service = CategoryService(db)
    return await service.update_category(category_id, category)
