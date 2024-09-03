from http import HTTPStatus
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth import create_access_token, create_email_verification_token, hash_password, verify_password, verify_token
from utils.helpers.enums import Status
from repository.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin
from utils.email.send_email import send_verification_email

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate, db: AsyncSession):
        try:
            user.validate_passwords()
            
            existing_user_by_email = await self.repository.get_user_by_email(user.email, db)
            if existing_user_by_email:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT, 
                    content={"message": f"User with email {user.email} already exists"}
                )

            existing_user_by_username = await self.repository.get_user_by_username(user.username, db)
            if existing_user_by_username:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT, 
                    content={"message": f"User with username {user.username} already exists"}
                )
            
            hashed_password = hash_password(user.password)

            user_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password": hashed_password,
            }

            new_user = await self.repository.create_user(user_data, db)
            
            verification_token = create_email_verification_token(new_user.id)
            await send_verification_email(user.email, verification_token)

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
            
            token, expire_in = create_access_token(user.id)
            
            if not token:
                return JSONResponse(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    content={"message": "Could not create access token. Please try again"}
                )
            
            return JSONResponse(
                status_code=HTTPStatus.OK, 
                content={"message": "Login successful", "access_token": token, "token_type": "bearer", "expire_in": expire_in}
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
                    content={"message": "Invalid token"}
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
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

