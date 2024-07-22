from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from app.models.pydantics.base_model import TokenResponse, TokenPayload
from app.models.pydantics.user_pydantics import (
    UserResponse,
    UserCreate,
    UserUpdate,
    UserLogin,
    ChangePasswordRequest
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.user_service import UserService
from app.database import get_database
from app.utils.JWTToken import JWTBearer

user_router = APIRouter(prefix="/users", tags=['Users'])


@user_router.post('/', response_model=TokenResponse)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    service = UserService(db)
    return await service.create_user(user)


@user_router.get('/', response_model=UserResponse)
async def get_user_details(
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        return await service.retrieve_user(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.post('/login', response_model=TokenResponse)
async def login_user(user: UserLogin, db: AsyncIOMotorClient = Depends(get_database)):
    service = UserService(db)
    return await service.login_user(user)


@user_router.post('/change_password', status_code=201)
async def change_password(password_request: ChangePasswordRequest, db: AsyncIOMotorClient = Depends(get_database),
                          token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.change_user_password(password_request, token)


@user_router.post('/change_email', status_code=201)
async def change_email(new_email: EmailStr, db: AsyncIOMotorClient = Depends(get_database),
                       token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.change_email(new_email, token)


@user_router.post('/verify_otp', status_code=200)
async def verify_otp(otp: str, db: AsyncIOMotorClient = Depends(get_database),
                     token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.verify_otp(otp, token)


@user_router.put('/', response_model=UserResponse)
async def update_user(
        book: UserUpdate,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        return await service.update_user(user.id, book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.put('/admin/update_user_role', status_code=201)
async def update_user_role(
        user_id: str,
        role: List[str],
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    try:
        service = UserService(db)
        return await service.update_user_role(user_id, role, user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete('/', status_code=204)
async def delete_user(
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        await service.delete_user(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete('/admin/delete_user', status_code=204)
async def delete_user(
        user_id: str,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = UserService(db)
        await service.delete_user_by_admin(user_id,user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
