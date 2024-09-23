from sqlalchemy import String, Column, Integer, Boolean, DateTime
from datetime import datetime

from src.db.legacy.base_model import BaseModel
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, default=False)

    # Example relationship (if users have related items like posts)
    # posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
