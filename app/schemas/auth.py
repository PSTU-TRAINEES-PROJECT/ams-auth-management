import re
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

class Token(BaseModel):
    message: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expire_in: Optional[int] = None

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "strongpassword123"
            }
        }

class UserCreate(BaseModel):
    username: constr(min_length=3) # type: ignore
    first_name: constr(min_length=3) # type: ignore
    last_name: constr(min_length=3) # type: ignore
    email: EmailStr
    password: constr(min_length=8) # type: ignore
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "John",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "password": "strongpassword123",
                "confirm_password": "strongpassword123"
            }
        }
    
    @validator('password')
    def password_complexity(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[^\w\s]', value):
            raise ValueError('Password must contain at least one special character')
        return value

    def validate_passwords(self):
        if self.password == self.confirm_password:
            return True
        else:
            return False
