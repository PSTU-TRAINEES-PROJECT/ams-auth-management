from schemas.base import Base
from schemas.users import current_time
from sqlalchemy import Column, DateTime, Integer, String


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_time, nullable=False, onupdate=current_time)
    deleted_at = Column(DateTime(timezone=True), nullable=True)