from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.jwt_handler import create_access_token, verify_token, create_email_verification_token
from utils.helpers.converters import hash_password, verify_password
from repository.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin
from utils.email.send_email import send_verification_email

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate, db: AsyncSession):
        user.validate_passwords()
        
        existing_user_by_email = await self.repository.get_user_by_email(user.email, db)
        if existing_user_by_email:
            raise ValueError(f"User with email {user.email} already exists")

        existing_user_by_username = await self.repository.get_user_by_username(user.username, db)
        if existing_user_by_username:
            raise ValueError(f"User with username {user.username} already exists")
        hashed_password = hash_password(user.password)

        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hashed_password,
        }

        new_user = await self.repository.save_user(user_data, db)
        
        verification_token = create_email_verification_token(user.email)
        await send_verification_email(user.email, verification_token)

        return new_user

    async def authenticate_user(self, login_data: UserLogin, db: AsyncSession):
        user = await self.repository.get_user_by_email(login_data.email, db)
        
        if not user.email_verified:
            raise ValueError("Please verify your email first")
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        token, expire_in = create_access_token(user.email)
        return token, expire_in
    
    async def verify_email(self, token: str, db: AsyncSession):
        email = verify_token(token)
        if not email:
            raise ValueError("Invalid token")
        
        user = await self.repository.get_user_by_email(email, db)
        if not user:
            raise ValueError("User not found")

        await self.repository.update_user_email_verification(user, db)

