from sqlalchemy import String, UUID, Column, DateTime, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
import uuid

from src.db.config import Base

            
class BaseModel(Base):
    """
    This class serves as a base model for all other database models in the application.
    It provides common fields such as id, created_at, updated_at, and status.

    Attributes:
    - id (UUID): Unique identifier for each record.
    - created_at (DateTime): Timestamp indicating when the record was created.
    - updated_at (DateTime): Timestamp indicating when the record was last updated.
    - status (Boolean): Indicates the current status of the record.
    """

    __abstract__ = True

    uuid = Column(UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(
        DateTime, nullable=True, default=func.now(), onupdate=func.now()
    )
    status = Column(Boolean, nullable=True, default=True)

    def __repr__(self):
        raise NotImplementedError("Please implement the description of the table")
