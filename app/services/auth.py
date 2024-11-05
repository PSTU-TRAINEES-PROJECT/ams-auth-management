from http import HTTPStatus
import secrets
from typing import Dict
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from config import get_config
from utils.helpers.get_enum import enum_to_dict
from core.auth import create_access_token, create_email_verification_token, hash_password, verify_password, \
    verify_token, create_refresh_token
from utils.helpers.enums import Status, Role, PlatformTypes
from repository.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin
from utils.email.send_email import send_verification_email
import jwt


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate, db: AsyncSession, background_tasks: BackgroundTasks):
        try:
            if not user.validate_passwords():
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": "Passwords & confirm passwords do not match"}
                )

            existing_user_by_email = await self.repository.get_user_by_email(user.email, db)
            if existing_user_by_email:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": f"User with email {user.email} already exists"}
                )

            hashed_password = hash_password(user.password)

            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": hashed_password,
            }

            new_user = await self.repository.create_user(user_data, db)

            verification_token = create_email_verification_token(new_user.id)
            background_tasks.add_task(send_verification_email, user.first_name, user.email, verification_token)

            return JSONResponse(
                status_code=HTTPStatus.CREATED,
                content={"message": "User created successfully", "data": new_user.to_dict()}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def authenticate_user(self, login_data: UserLogin, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_email(login_data.email, db)

            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )

            if not user.email_verified:
                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content={"message": "Please verify your email first"}
                )

            if user.status == Status.INACTIVE.value:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"message": "Your account is inactive"}
                )

            if not verify_password(login_data.password, user.password_hash):
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"message": "Invalid password"}
                )

            access_token, access_token_expire_in = create_access_token(user.id)
            refresh_token, refresh_token_expire_in = create_refresh_token(user.id)

            if not access_token:
                return JSONResponse(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    content={"message": "Could not create access token. Please try again"}
                )

            if not refresh_token:
                return JSONResponse(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    content={"message": "Could not create access token. Please try again"}
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "aceess_token_expire_in": access_token_expire_in,
                    "refresh_token_expire_in": refresh_token_expire_in
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def verify_email_token(self, token: str, db: AsyncSession):
        try:
            user_id = verify_token(token)

            if not user_id:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "Invalid token subject"}
                )

            user = await self.repository.get_user_by_user_id(user_id, db)

            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )

            if user.email_verified:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": "Email already verified"}
                )

            await self.repository.update_user_email_verification(user, db)
            await self.repository.update_user_status_to_active(user, db)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "Email verified successfully"}
            )
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Email Verification Token expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Invalid email verification token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def refresh_access_token(self, refresh_token: str, db: AsyncSession):
        try:
            user_id = verify_token(refresh_token)

            if not user_id:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "Invalid token subject"}
                )

            user_id = int(user_id)
            user = await self.repository.get_user_by_user_id(user_id, db)

            if user is None:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )

            access_token, access_token_expire_in = create_access_token(user_id)
            new_refresh_token, refresh_token_expire_in = create_refresh_token(user.id)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Token refreshed successfully",
                    "access_token": access_token,
                    "refresh_token": new_refresh_token,
                    "token_type": "bearer",
                    "aceess_token_expire_in": access_token_expire_in,
                    "refresh_token_expire_in": refresh_token_expire_in
                }
            )

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Refresh token expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Invalid refresh token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def validate_user_token(self, token: str, db: AsyncSession):
        try:
            user_id = verify_token(token)
            
            if not user_id:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "Invalid token subject"}
                )

            user = await self.repository.get_user_by_user_id(user_id, db)

            if user is None:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User token is valid" , "id": user.id, "email": user.email}
            )

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Token expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={"message": "Invalid token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )


    async def google_login(self, auth_code: str, db: AsyncSession):
        try:
            google_client_id = get_config().google_client_id
            google_client_secret = get_config().google_client_secret

            token_data = {
                'code': auth_code,
                'client_id': google_client_id,
                'client_secret': google_client_secret,
                'redirect_uri': 'postmessage',
                'grant_type': 'authorization_code'
            }

            token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
            if token_response.status_code != 200:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "Failed to validate Google OAuth2 token"}
                )

            token_info = token_response.json()
            
            headers = {'Authorization': f'Bearer {token_info["access_token"]}'}
            userinfo_response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
            user_info = userinfo_response.json()

            user = await self.repository.get_user_by_email(user_info['email'], db)

            if not user:
                user_data = {
                    "email": user_info['email'],
                    "first_name": user_info['given_name'],
                    "last_name": user_info['family_name'],
                    "password": hash_password(secrets.token_urlsafe(32)), 
                    "email_verified": True 
                }
                user = await self.repository.create_user(user_data, db)
                await self.repository.update_user_status_to_active(user, db)

            access_token, access_token_expire_in = create_access_token(user.id)
            refresh_token, refresh_token_expire_in = create_refresh_token(user.id)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Google login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "aceess_token_expire_in": access_token_expire_in,
                    "refresh_token_expire_in": refresh_token_expire_in
                }
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )




    async def get_all_enums(self) -> Dict:
        try:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Enums fetched successfully",
                    "status": enum_to_dict(Status),
                    "role": enum_to_dict(Role),
                    "platformTypes": enum_to_dict(PlatformTypes)
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )