import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base
from sqlalchemy.orm import relationship

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)          # Renombrado
    application_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)  # Renombrado
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Restricción: un usuario solo puede calificar una aplicación una vez
    __table_args__ = (
        UniqueConstraint('user_id', 'application_id', name='uq_feedback_user_app'),
        Index('ix_feedback_app', 'application_id'),
        Index('ix_feedback_user', 'user_id'),
    )

    # Relaciones
    user = relationship('User', back_populates='feedbacks')
    application = relationship('Application', back_populates='feedbacks')