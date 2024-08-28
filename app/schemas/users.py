from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pytz

Base = declarative_base()

def current_time():
    return datetime.datetime.now(tz=pytz.timezone('UTC'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    email = Column(String(100), index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    password_hash = Column(String(255))
    mobile = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_time, nullable=False, onupdate=current_time)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


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
