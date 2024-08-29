from utils.helpers.converters import hash_password, verify_password
from repository.user_repository import UserRepository
from schemas.auth import UserCreate
from sqlalchemy.ext.asyncio import  AsyncSession

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate, db: AsyncSession):
        user.validate_passwords()
        
        # Check if user already exists
        existing_user = await self.repository.get_user_by_email(user.email, db)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = hash_password(user.password)

        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": hashed_password,
        }

        return await self.repository.save_user(user_data, db)
    
    async def get_all_users(self, db: AsyncSession):
        return await self.repository.get_all_users(db)