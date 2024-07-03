from fastapi import APIRouter, HTTPException, Depends

from app.api.endpoints.review_routers import get_current_username
from app.models.pydantics.user_pydantics import (
    UserResponse,
    UserCreate,
    UserUpdate
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.user_service import UserService
from app.database import get_database
from typing import List, Annotated

user_router = APIRouter(prefix="/users", tags=['Users'])


@user_router.get('/', response_model=List[UserResponse])
async def retrieve_user(
        user_id: str = Depends(get_current_username),
        db: AsyncIOMotorClient = Depends(get_database)
):
    service = UserService(db)
    return await service.retrieve_users()


@user_router.post('/', response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    service = UserService(db)
    return await service.create_user(user)


@user_router.get('/{user_id}', response_model=UserResponse)
async def retrieve_user(
        user_id: Annotated[str, Depends(get_current_username)],
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        return await service.retrieve_user(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put('/{user_id}', response_model=UserResponse)
async def update_user(
        book: UserUpdate,
        user_id: str = Depends(get_current_username),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        return await service.update_user(user_id, book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete('/{user_id}', status_code=204)
async def delete_user(
        user_id: str = Depends(get_current_username),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        await service.delete_user(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
