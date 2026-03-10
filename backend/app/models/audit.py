from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from enum import Enum
from datetime import datetime
import uuid

class LoginStatusEnum(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"

class LoginAuditLog(BaseModel):
    __tablename__ = "login_audit_log"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ip_address = Column(INET, nullable=False)
    user_agent = Column(Text)
    status = Column(SQLEnum(LoginStatusEnum), nullable=False)
    failure_reason = Column(Text)  # For failed logins
    session_id = Column(String(255))  # For tracking sessions
    
    # Relationships
    user = relationship("User", back_populates="login_audits")
    
    def __repr__(self):
        return f"<LoginAuditLog(user_id='{self.user_id}', status='{self.status}')>"