from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class FeedbackBase(BaseModel):
    fee_use_id: UUID
    fee_app_id: UUID
    fee_rating: int = Field(..., ge=1, le=5)
    fee_comment: Optional[str]
    fee_date: Optional[datetime]

class FeedbackCreate(FeedbackBase):
    """Usado para crear nuevo feedback."""
    pass

class FeedbackUpdate(BaseModel):
    fee_rating: Optional[int] = Field(None, ge=1, le=5)
    fee_comment: Optional[str]

class FeedbackRead(FeedbackBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True