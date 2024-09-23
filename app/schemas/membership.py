from sqlalchemy import Column, ForeignKey, Integer, String
from schemas.base import Base


class Membership(Base):
    __tablename__ = "memberships"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), primary_key=True, nullable=False)
    role = Column(String(50), nullable=False)