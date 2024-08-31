from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
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
        return JSONResponse(content={"message": "User registered successfully", "user": new_user}, status_code=201)
    except ValueError as e:
        raise e
    except Exception as e:
        raise e


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token, expire_in = await auth_service.authenticate_user(user, db)
        
        if not token:
            return JSONResponse(status_code=401, content={"message": "Invalid email or password"})
        
        return JSONResponse(content={"message": "Login successful", "access_token": token, "token_type": "bearer", "expire_in": expire_in}, status_code=200)
    except ValueError as e:
        raise e
    except Exception as e:
        raise e


@auth_router.post("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        await auth_service.verify_email(token, db)
        return JSONResponse(content={"message": "Email verified successfully"}, status_code=200)
    except ValueError as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e

