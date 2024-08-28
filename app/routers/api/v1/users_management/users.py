from fastapi import APIRouter, HTTPException
from schemas.users import UserCreate
from repository.user_repository import UserRepository
from services.users import UserService

user_router = APIRouter()

repository = UserRepository()  # Using mock repository for now
user_service = UserService(repository)

@user_router.post("/signup")
async def signup(user: UserCreate):
    try:
        new_user = user_service.create_user(user)
        return {"msg": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# # this temporary endpoint to retrieve all users
# @user_router.get("/users")
# async def get_users():
#     return repository.mock_db  # Directly return the mock database contents
