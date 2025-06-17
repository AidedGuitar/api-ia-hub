from datetime import datetime
from sqlalchemy import (Column, DateTime, ForeignKey, Index, Enum as SAEnum)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base
import enum
import uuid

class InteractionType(str, enum.Enum):
    view = "view"
    click = "click"
    favorite = "favorite"
    feedback = "feedback"

class Interaction(Base):
    __tablename__ = 'interaction'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    int_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    int_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    int_type = Column(SAEnum(InteractionType, name="interaction_type"), nullable=False)
    int_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # índices compuestos para búsquedas frecuentes
    __table_args__ = (
        Index('ix_interaction_user_app', 'int_use_id', 'int_app_id'),
        Index('ix_interaction_timestamp', 'int_timestamp'),
    )