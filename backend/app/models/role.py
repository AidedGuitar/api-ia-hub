from sqlalchemy import Column, Integer, String
from .base import Base

class Role(Base):
    __tablename__ = 'role'

    rol_id = Column(Integer, primary_key=True, autoincrement=True)
    rol_name = Column(String(50), nullable=False)
