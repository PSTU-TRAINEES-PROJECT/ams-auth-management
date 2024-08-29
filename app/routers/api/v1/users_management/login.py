from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repository.database import get_db
from services.auth import LoginService
from repository.user_repository import UserRepository
from schemas.auth import UserLogin, Token

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
