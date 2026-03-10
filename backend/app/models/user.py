from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from datetime import datetime
import uuid

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(INET)
    
    # Foreign key to roles
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    login_audits = relationship("LoginAuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(email='{self.email}', username='{self.username}')>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

class UserSettings(BaseModel):
    __tablename__ = "user_settings"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    notification_email = Column(Boolean, default=True)
    notification_push = Column(Boolean, default=False)
    theme = Column(String(20), default="light")
    
    # Relationships
    user = relationship("User", back_populates="settings")
    
    def __repr__(self):
        return f"<UserSettings(user_id='{self.user_id}')>"