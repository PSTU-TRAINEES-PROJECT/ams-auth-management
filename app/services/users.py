from utils.helpers.enums import Status
from repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import  AsyncSession

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self, db: AsyncSession):
        return await self.repository.get_all_users(db)
    
    async def update_user_status(self, user_id: int, status: Status, db: AsyncSession):
        user = await self.repository.get_user_by_user_id(user_id, db)
        
        if not user:
            raise ValueError("User not found")
        
        await self.repository.update_user_status(user, status, db)