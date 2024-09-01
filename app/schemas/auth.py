from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class Token(BaseModel):
    message: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expire_in: Optional[int] = None

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
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

    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords & confirm passwords do not match")
