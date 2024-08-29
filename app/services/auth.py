from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.jwt_handler import create_access_token
from utils.helpers.converters import verify_password
from repository.user_repository import UserRepository
from schemas.auth import UserLogin

class LoginService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def authenticate_user(self, login_data: UserLogin, db: AsyncSession):
        user = await self.repository.get_user_by_email(login_data.email, db)
        if not user or not verify_password(login_data.password, user.password_hash):
            return None
        return create_access_token({"sub": user.email})