from fastapi import APIRouter
from app.models.pydantics.auth_pydantics import UserCreate
from motor.motor_asyncio import AsyncIOMotorClient

from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@auth_router.post('/', status_code=201)
async def create_user(user: UserCreate, db: AsyncIOMotorClient):
    service = AuthService(db)
    return service.create_user(user)
