from sqlalchemy import Column, String, Boolean, BigInteger, UUID
from sqlalchemy.orm import relationship
import uuid
from src.db.legacy.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    # UUID as the primary key
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    telegram_id = Column(BigInteger, nullable=True)
    telegram_username = Column(String(128), nullable=True)
    is_superuser = Column(Boolean, default=False)

    # One-to-many relationship to Notes
    notes = relationship("Notes", back_populates="author")      

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
