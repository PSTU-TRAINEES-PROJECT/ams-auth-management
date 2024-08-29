from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pytz

class Token(BaseModel):
    access_token: str
    token_type: str

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
