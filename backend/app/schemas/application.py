from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ApplicationBase(BaseModel):
    app_name: str
    app_category: Optional[str]
    app_link: str = Field(..., pattern=r"^https?://")
    app_description: Optional[str]
    app_source: Optional[str]
    app_keywords: Optional[str]
    app_academic_level: Optional[str]

class ApplicationCreate(ApplicationBase):
    # for manual: app_source="manual"; for IA: app_source="ia"
    pass

class ApplicationUpdate(BaseModel):
    app_name: Optional[str]
    app_category: Optional[str]
    app_link: str = Field(..., pattern=r"^https?://")
    app_description: Optional[str]
    app_source: Optional[str]
    app_keywords: Optional[str]
    app_academic_level: Optional[str]

class ApplicationRead(ApplicationBase):
    id: UUID
    avg_rating: float | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
