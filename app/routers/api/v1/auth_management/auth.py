from fastapi import APIRouter, Depends, BackgroundTasks
from repository.database import get_db
from schemas.auth import GoogleLogin, UserCreate, UserLogin, Token
from repository.user_repository import UserRepository
from services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()
repository = UserRepository()
auth_service = AuthService(repository)

@auth_router.post("/signup")
async def signup(user: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    return await auth_service.create_user(user, db, background_tasks)

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


@auth_router.post("/google-login")
async def google_login(login_data: GoogleLogin, db: AsyncSession = Depends(get_db)):
    return await auth_service.google_login(login_data.code, db)


@auth_router.get("/get-all-enums")
async def get_all_enums():
    return await auth_service.get_all_enums()


