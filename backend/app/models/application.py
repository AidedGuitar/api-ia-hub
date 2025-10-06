import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Application(Base):
    __tablename__ = 'application'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(String(100), nullable=False, unique=True)   # evita duplicados
    app_category = Column(String(100), nullable=True)   # p.ej. "Matemáticas", "Humanidades"
    app_link = Column(Text, nullable=False) 
    app_description = Column(Text, nullable=True)
    app_source = Column(String(50), nullable=True)  # p.ej. "manual" o "ia"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación inversa para feedbacks e interacciones
    feedbacks = relationship('Feedback', back_populates='application', cascade='all, delete-orphan')
    interactions = relationship('Interaction', back_populates='application', cascade='all, delete-orphan')