from sqlalchemy import Column, String, Text, ForeignKey, UUID
from sqlalchemy.orm import relationship, mapped_column
import uuid
from src.db.legacy.base_model import BaseModel


class Notes(BaseModel):
    __tablename__ = "notes"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = relationship("User", back_populates="notes")
    author_id = mapped_column(ForeignKey("users.uuid"), nullable=False)

    def __repr__(self):
        return f"<Notes(title={self.title}, author_id={self.author_id})>"
