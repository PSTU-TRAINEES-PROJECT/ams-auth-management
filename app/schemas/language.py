from sqlalchemy import Column, String
from schemas.base import Base


class Language(Base):
    __tablename__ = "languages"

    code = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)