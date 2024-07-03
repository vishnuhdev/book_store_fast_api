from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from typing import List
from app.models.pydantics.author_pydantics import (
    AuthorResponse,
    CreateAuthor,
    UpdateAuthor
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_database
from app.services.author_service import AuthorService

author_router = APIRouter(prefix="/authors", tags=['authors'])


@author_router.get('/', response_model=List[AuthorResponse])
async def retrieve_authors(db: AsyncIOMotorClient = Depends(get_database)):
    service = AuthorService(db)
    return await service.retrieve_authors()


@author_router.post('/', response_model=AuthorResponse, status_code=201)
async def create_author(author: CreateAuthor, db: AsyncIOMotorClient = Depends(get_database)):
    service = AuthorService(db)
    return await service.create_author(author)


@author_router.get('/{author_id}', response_model=AuthorResponse)
async def retrieve_author(
        author_id: str, db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = AuthorService(db)
        return await service.retrieve_author(author_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@author_router.put('/{author_id}', response_model=AuthorResponse)
async def update_author(
        author_id: str, author: UpdateAuthor, db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        service = AuthorService(db)
        return await service.update_author(author_id, author)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
