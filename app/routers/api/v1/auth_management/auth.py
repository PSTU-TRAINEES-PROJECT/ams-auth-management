from fastapi import APIRouter, Depends, HTTPException, status
from repository.database import get_db
from schemas.auth import UserCreate, UserLogin, Token
from repository.user_repository import UserRepository
from services.auth import AuthService
from sqlalchemy.ext.asyncio import  AsyncSession

auth_router = APIRouter()
repository = UserRepository()
auth_service = AuthService(repository)

@auth_router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await auth_service.create_user(user, db)
        return {"message": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token, expire_in = await auth_service.authenticate_user(user, db)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful", "access_token": token, "token_type": "bearer", "expire_in": expire_in}
