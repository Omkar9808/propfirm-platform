import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class UUIDMixin:
    """Mixin to add UUID primary key"""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

class BaseModel(Base, UUIDMixin, TimestampMixin):
    """Base model with UUID primary key and timestamps"""
    __abstract__ = True
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            elif isinstance(value, datetime):
                result[column.name] = value.isoformat() if value else None
            else:
                result[column.name] = value
        return result