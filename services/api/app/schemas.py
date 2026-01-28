from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class EntryCreate(BaseModel):
    kind: str
    title: str
    notes: str | None = None

class EntryOut(BaseModel):
    id: UUID
    kind: str
    title: str
    notes: str | None
    is_favorite: bool
    status: str
    cv_result: dict | None
    created_at: datetime

    class Config:
        from_attributes = True
