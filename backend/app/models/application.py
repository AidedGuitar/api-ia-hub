import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Application(Base):
    __tablename__ = 'application'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), nullable=False)
    app_category = Column(String(100))
    app_link = Column(Text, nullable=False)
    app_description = Column(Text)
    app_source = Column(String(50))
