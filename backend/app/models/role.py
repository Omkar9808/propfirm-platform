from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from enum import Enum
import uuid

class RoleEnum(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    TRADER = "trader"
    GUEST = "guest"

class Role(BaseModel):
    __tablename__ = "roles"
    
    name = Column(SQLEnum(RoleEnum), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(name='{self.name}')>"