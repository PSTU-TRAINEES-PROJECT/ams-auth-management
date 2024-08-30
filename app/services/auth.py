from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.jwt_handler import create_access_token
from utils.helpers.converters import hash_password, verify_password
from repository.user_repository import UserRepository
from schemas.auth import UserCreate, UserLogin

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

        return await self.repository.save_user(user_data, db)

    async def authenticate_user(self, login_data: UserLogin, db: AsyncSession):
        user = await self.repository.get_user_by_email(login_data.email, db)
        if not user or not verify_password(login_data.password, user.password_hash):
            return None, None
        return create_access_token(user.email)