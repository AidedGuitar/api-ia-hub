from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base

class Interaction(Base):
    __tablename__ = 'interaction'

    int_id = Column(Integer, primary_key=True, autoincrement=True)
    int_use_id = Column(UUID(as_uuid=True), ForeignKey('user.use_id'), nullable=False)
    int_app_id = Column(UUID(as_uuid=True), ForeignKey('application.app_id'), nullable=False)
    int_type = Column(String(50))
    int_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
