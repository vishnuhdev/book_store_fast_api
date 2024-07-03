from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_database
from app.services.user_service import UserService

security = HTTPBasic()


async def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        db: AsyncIOMotorClient = Depends(get_database)
):
    user_service = UserService(db)
    user = await user_service.retrieve_user_with_credentials(credentials.username, credentials.password)
    return user['id']
