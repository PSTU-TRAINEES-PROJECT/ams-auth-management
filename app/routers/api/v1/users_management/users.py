from fastapi import APIRouter, Depends
from repository.database import get_db
from repository.user_repository import UserRepository
from services.users import UserService
from sqlalchemy.ext.asyncio import  AsyncSession

user_router = APIRouter()
repository = UserRepository()
user_service = UserService(repository)


@user_router.get("/all-users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(db)
    return users


