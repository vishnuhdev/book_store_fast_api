from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models.pydantics.user_pydantics import UserResponse, UserCreate
from app.models.db.user_model import User
from bson import ObjectId
from fastapi import HTTPException


class UserService:

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = self.db.users

    async def retrieve_user_with_credentials(self, email, password):
        user_from_email = await self.collection.find_one({'email': email})
        if not user_from_email:
            raise HTTPException(status_code=403, detail='Invalid user email.')
        is_password_matched = user_from_email['password'] == password
        if not is_password_matched:
            raise HTTPException(status_code=401, detail='Invalid password.')
        return self.__replace_id(user_from_email)

    async def retrieve_users(self) -> List[UserResponse]:
        result = self.collection.find()
        users = []
        async for user in result:
            user = self.__replace_id(user)
            users.append(UserResponse(**user))
        return users

    async def create_user(self, userRequest: UserCreate) -> UserResponse:
        user_dict = userRequest.dict()
        user = User(**user_dict)
        inserted = await self.collection.insert_one(user.dict())
        return await self.retrieve_user(str(inserted.inserted_id))

    async def retrieve_user(self, user_id: str) -> UserResponse:
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        user = self.__replace_id(user)
        return UserResponse(**user)

    async def update_user(self, user_id, user):
        if not await self.collection.find_one({'_id': ObjectId(user_id)}):
            raise HTTPException(status_code=404, detail='User not found.')
        user_dict = user.dict(exclude_unset=True)
        result = await self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})
        return await self.retrieve_user(user_id)

    async def delete_user(self, user_id: str) -> None:
        if not await self.collection.find_one({'_id': ObjectId(user_id)}):
            raise HTTPException(status_code=404, detail='User not found.')
        await self.collection.delete_one({'_id': ObjectId(user_id)})

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
