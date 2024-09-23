from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
import datetime
import pytz
from schemas.base import Base
from utils.helpers.enums import Status

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
    email_verified = Column(Boolean, default=False)
    mobile = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_time, nullable=False, onupdate=current_time)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    status = Column(Enum(Status), nullable=False, default=Status.INACTIVE.value, server_default=Status.INACTIVE.value)


    language_code = Column(String(10), ForeignKey('languages.code'), nullable=True)  # Nullable


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_verified": self.email_verified,
            "mobile": self.mobile,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "status": self.status,
            "language_code": self.language_code if self.language_code else None
        }





