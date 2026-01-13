from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MangaJobBase(BaseModel):
    theme: str


class MangaJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    manga_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


class MangaJobCreate(MangaJobBase):
    pass