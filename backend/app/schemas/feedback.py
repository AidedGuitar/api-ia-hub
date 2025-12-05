from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.user import UserBase

class FeedbackBase(BaseModel):
    user_id: UUID
    application_id: UUID
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
    user: UserBase
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True