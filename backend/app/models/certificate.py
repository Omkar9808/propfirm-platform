from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
import uuid
from datetime import datetime

class Certificate(BaseModel):
    __tablename__ = "certificates"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    certificate_type = Column(String(50), nullable=False)  # e.g., "profit_target_achieved", "risk_rule_passed"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    certificate_data = Column(Text)  # JSON string with certificate details
    issued_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True))
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(50), unique=True)
    template_url = Column(String(500))  # URL to certificate template/image
    
    # Relationships
    user = relationship("User")
    account = relationship("Account")
    
    def __repr__(self):
        return f"<Certificate(user_id='{self.user_id}', type='{self.certificate_type}', verified={self.is_verified})>"