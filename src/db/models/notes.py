from sqlalchemy import String, Integer, Column, Text

from src.db.legacy.base_model import BaseModel


class Notes(BaseModel):
    __tablename__ = "notes"
    # identifier, title, content, tags, creation date, and last modification date

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
