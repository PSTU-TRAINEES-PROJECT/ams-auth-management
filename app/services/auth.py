from datetime import datetime, timedelta
from pydantic import EmailStr
from config import get_config
from http import HTTPStatus
from fastapi.responses import JSONResponse
import jwt
from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import Status
from utils.helpers.converters import hash_password, verify_password
from repository.user_repository import UserRepository  # Add this line
from schemas.auth import UserCreate, UserLogin
from utils.email.send_email import send_verification_email
from config import get_config


# JWT configuration
JWT_SECRET_KEY = get_config().jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = get_config().access_token_expire_minutes
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = get_config().email_verification_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = get_config().refresh_token_expire_days

# JWT token creation and verification functions
def create_access_token(user_id: int):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, int(expire.timestamp())

def create_email_verification_token(user_id: int):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")


# Rest of the AuthService class and methods as they were before
# No need to import jwt handler functions anymore as they are now part of this file
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
            
            access_token, expire_in = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            
            if not access_token:
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
                    "expire_in": expire_in
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


    async def refresh_access_token(self, refresh_token: str, db: AsyncSession):
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            
            if not user_id or not user_id.isdigit():
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid token subject")
            
            user_id = int(user_id)

            user = await self.repository.get_user_by_user_id(user_id, db)

            if user is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

            access_token, expire_in = create_access_token(user_id)
            return {"access_token": access_token, "token_type": "bearer", "expire_in": expire_in}

        except JWTError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Invalid token: {str(e)}")
