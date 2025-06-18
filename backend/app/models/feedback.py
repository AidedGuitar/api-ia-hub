import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base
from sqlalchemy.orm import relationship

class Feedback(Base):
    __tablename__ = 'feedback'
    __table_args__ = (
        UniqueConstraint('fee_use_id', 'fee_app_id', name='uq_feedback_user_app'),
        Index('ix_feedback_app', 'fee_app_id'),
        Index('ix_feedback_user', 'fee_use_id'),
    )


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fee_use_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    fee_app_id = Column(UUID(as_uuid=True), ForeignKey('application.id'), nullable=False)
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='feedbacks')
    application = relationship('Application', back_populates='feedbacks')