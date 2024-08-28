from fastapi import APIRouter, Depends, HTTPException
from repository.database import get_db
from schemas.users import UserCreate
from repository.user_repository import UserRepository
from services.users import UserService
from sqlalchemy.ext.asyncio import  AsyncSession

user_router = APIRouter()

repository = UserRepository()
user_service = UserService(repository)

@user_router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await user_service.create_user(user, db)
        return {"message": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("/all-users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(db)
    return users