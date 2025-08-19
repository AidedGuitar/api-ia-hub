from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.interaction import InteractionType

class InteractionBase(BaseModel):
    int_use_id: UUID
    int_app_id: UUID
    int_type: InteractionType
    int_timestamp: Optional[datetime] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionUpdate(BaseModel):
    int_type: Optional[InteractionType]

class InteractionRead(InteractionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True