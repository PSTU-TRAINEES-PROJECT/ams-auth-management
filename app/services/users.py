from repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import  AsyncSession

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self, db: AsyncSession):
        return await self.repository.get_all_users(db)