from fastapi import APIRouter, Depends
from repository.database import get_db
from schemas.auth import UserCreate, UserLogin, Token
from repository.user_repository import UserRepository
from services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()
repository = UserRepository()
auth_service = AuthService(repository)

@auth_router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_service.create_user(user, db)

@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_service.authenticate_user(user, db)

@auth_router.post("/verify-email")
async def verify_email_token(token: str, db: AsyncSession = Depends(get_db)):
    return await auth_service.verify_email_token(token, db)

@auth_router.post("/refresh-token")
async def renew_refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    return await auth_service.refresh_access_token(refresh_token, db)

@auth_router.post("/validate_token")
async def validate_user_token(token:str,db:AsyncSession = Depends(get_db)):
    return await auth_service.validate_user_token(token,db)