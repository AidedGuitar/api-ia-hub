from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base

class Feedback(Base):
    __tablename__ = 'feedback'

    fee_id = Column(Integer, primary_key=True, autoincrement=True)
    fee_use_id = Column(UUID(as_uuid=True), ForeignKey('user.use_id'), nullable=False)
    fee_app_id = Column(UUID(as_uuid=True), ForeignKey('application.app_id'), nullable=False)
    fee_rating = Column(Integer, CheckConstraint('fee_rating >= 1 AND fee_rating <= 5'))
    fee_comment = Column(Text)
    fee_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
