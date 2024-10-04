from pydantic import BaseModel, UUID4
from datetime import datetime


class NoteScheme(BaseModel):
    title: str
    content: str


class NoteUpdateScheme(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponseScheme(NoteScheme):
    uuid: UUID4
    author_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
