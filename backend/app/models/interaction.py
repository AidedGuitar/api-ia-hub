from datetime import datetime
from sqlalchemy import (Column, DateTime, String, ForeignKey, Index)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base
import enum
import uuid
from sqlalchemy.orm import relationship

class InteractionType(str, enum.Enum):
    view = "view"
    click = "click"
    favorite = "favorite"
    feedback = "feedback"

class Interaction(Base):
    __tablename__ = 'interaction'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)          # Renombrado
    application_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)  # Renombrado
    int_type = Column(String, nullable=False)  # Usamos String en lugar de SAEnum para simplificar
    int_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Índices para búsquedas frecuentes
    __table_args__ = (
        Index('ix_interaction_user_app', 'user_id', 'application_id'),
        Index('ix_interaction_timestamp', 'int_timestamp'),
    )

    # Relaciones
    user = relationship('User', back_populates='interactions')
    application = relationship('Application', back_populates='interactions')