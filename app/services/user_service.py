import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pyotp
from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from app.models.db.user_model import User
from app.models.pydantics.base_model import TokenResponse, TokenRequest, TokenPayload
from app.models.pydantics.user_pydantics import UserResponse, UserCreate, UserLogin, ChangePasswordRequest
from app.utils.util import create_access_token, create_refresh_token


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

    async def create_user(self, userRequest: UserCreate) -> TokenResponse:
        email = await self.collection.find_one({'email': userRequest.email})
        if email:
            raise HTTPException(status_code=403, detail='Email already registered.')
        user_dict = userRequest.dict()
        user_dict['role'] = ['user']
        user = User(**user_dict)
        inserted = await self.collection.insert_one(user.dict())
        token_request = TokenRequest(email=user.email, id=str(inserted.inserted_id))
        return TokenResponse(
            access_token=create_access_token(token_request),
            refresh_token=create_refresh_token(token_request)
        )

    async def login_user(self, userRequest: UserLogin) -> TokenResponse:
        user_db = await self.collection.find_one({'email': userRequest.email})
        if not user_db:
            raise HTTPException(status_code=403, detail='Invalid user email.')
        if user_db['password'] != userRequest.password:
            raise HTTPException(status_code=401, detail='Invalid password.')
        token_request = TokenRequest(email=userRequest.email, id=str(user_db['_id']))
        return TokenResponse(
            access_token=create_access_token(token_request),
            refresh_token=create_refresh_token(token_request)
        )

    async def retrieve_user(self, user_id: str) -> UserResponse:
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        user = self.__replace_id(user)
        if user['is_deleted']:
            raise HTTPException(status_code=403, detail='User not found')
        return UserResponse(**user)

    async def update_user(self, user_id, user):
        if not await self.collection.find_one({'_id': ObjectId(user_id)}):
            raise HTTPException(status_code=404, detail='User not found.')
        if user.email:
            is_email_exist = await self.collection.find_one({'email': user.email})
            if is_email_exist:
                raise HTTPException(status_code=404, detail='Email already exists.')
        user_dict = user.dict(exclude_unset=True)
        user_dict['updated_at'] = time.time()
        await self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})
        return await self.retrieve_user(user_id)

    async def change_user_password(self, password_request: ChangePasswordRequest, token: TokenPayload):
        user_db = await self.collection.find_one({'_id': ObjectId(token.id)})
        if not user_db:
            raise HTTPException(status_code=403, detail='Invalid user.')
        if user_db['password'] != password_request.current_password:
            raise HTTPException(status_code=401, detail='Incorrect old password.')
        user_db['password'] = password_request.new_password
        user_db['updated_at'] = time.time()
        await self.collection.update_one({'_id': ObjectId(token.id)},
                                         {'$set': {'password': password_request.new_password}})
        return JSONResponse(status_code=201, content='User password updated.')

    @staticmethod
    async def send_otp_email(email: str, otp: str):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL')
        sender_password = os.getenv('PASSWORD')

        if not sender_email or not sender_password:
            raise HTTPException(status_code=500, detail='Email credentials not configured.')

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "OTP Verification"
        body = f"Your OTP is {otp}"
        message.attach(MIMEText(body, "plain"))

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, message.as_string())
        except smtplib.SMTPException as e:
            raise HTTPException(status_code=500, detail=f'Failed to send email: {str(e)}')

    async def change_email(self, new_email: str, token: TokenPayload):
        user_db = await self.collection.find_one({'_id': ObjectId(token.id)})
        if not user_db:
            raise HTTPException(status_code=403, detail='Invalid user.')

        totp = pyotp.TOTP(os.getenv('OTP_SECRET'))
        otp = totp.now()

        await self.send_otp_email(new_email, otp)
        await self.collection.update_one(
            {'_id': ObjectId(token.id)},
            {'$set': {'temp_new_email': new_email, 'otp': otp}}
        )
        return JSONResponse(status_code=201, content='OTP sent successfully.')

    async def verify_otp(self, otp: str, token: TokenPayload):
        user_db = await self.collection.find_one({'_id': ObjectId(token.id)})
        if not user_db:
            raise HTTPException(status_code=403, detail='Invalid user.')

        if user_db.get('otp') != str(otp):
            raise HTTPException(status_code=401, detail='Invalid OTP.')

        await self.collection.update_one(
            {'_id': ObjectId(token.id)},
            {'$set': {'email': user_db['temp_new_email']}, '$unset': {'temp_new_email': "", 'otp': ""}}
        )
        return JSONResponse(status_code=200, content='Email updated successfully.')

    async def update_user_role(self, user_id, role, user):
        user_detail = await self.collection.find_one({'_id': ObjectId(user.id)})
        if not user_detail:
            raise HTTPException(status_code=404, detail='User not found.')
        if 'admin' not in user_detail['role']:
            raise HTTPException(status_code=403, detail='Only admin can update roles.')
        user = await self.collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail='User not found.')
        await self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': role}})
        return JSONResponse(status_code=200, content='User role updated successfully.')

    async def delete_user(self, user_id: str) -> None:
        user_details = await self.collection.find_one({'_id': ObjectId(user_id)})
        if not user_details:
            raise HTTPException(status_code=404, detail='User not found.')
        if user_id == str(user_details['_id']):
            await self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'is_deleted': True}})
        elif 'admin' in user_details['role']:
            await self.collection.delete_one({'_id': ObjectId(user_id)})

    async def delete_user_by_admin(self, user_id: str, admin_id: str):
        user = await self.collection.find_one({'_id': ObjectId(admin_id)})
        if not user:
            raise HTTPException(status_code=404, detail='User not found.')
        if 'admin' in user['role']:
            await self.collection.delete_one({'_id': ObjectId(user_id)})

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
