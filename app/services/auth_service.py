from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.pydantics.auth_pydantics import UserCreate, UserResponse
from app.models.db.user_model import User


class AuthService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.users

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_dict = user.dict()
        user = User(**user_dict)
        result = await self.collection.insert_one(user.dict())
        return await self.retrieve_user(str(result.inserted_id))

    async def retrieve_user(self, user_id: str) -> UserResponse:
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        user = self.__replace_id(user)
        return UserResponse(**user)

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
