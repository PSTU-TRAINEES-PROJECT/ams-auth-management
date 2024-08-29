from fastapi import APIRouter, Depends, HTTPException, status
from repository.database import get_db
from schemas.auth import UserCreate, UserLogin, Token
from repository.user_repository import UserRepository
from services.auth import LoginService
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


login_router = APIRouter()

@login_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    login_service = LoginService(repository=UserRepository())
    token = await login_service.authenticate_user(user, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}
