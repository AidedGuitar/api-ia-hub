import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_name = Column(String(100), nullable=False)
    use_email = Column(String(100), unique=True, nullable=False)
    use_career = Column(String(100))
    use_academic_level = Column(String(50))
    use_rol_id = Column(UUID(as_uuid=True), ForeignKey('role.id'), nullable=False)
    auth_provider = Column(String, default="local")  # 'local' o 'google'
    hashed_password = Column(String, nullable=True)  # <= AGREGAR ESTA LINEA
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación inversa para feedbacks e interacciones
    feedbacks = relationship('Feedback', back_populates='user',  cascade='all, delete-orphan')
    interactions = relationship('Interaction', back_populates='user', cascade='all, delete-orphan')