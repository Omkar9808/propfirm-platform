from sqlalchemy import Column, String, Text, Numeric, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from enum import Enum
import uuid
from datetime import datetime

class PayoutStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class PayoutType(str, Enum):
    AFFILIATE_COMMISSION = "affiliate_commission"
    TRADER_PAYOUT = "trader_payout"
    BONUS = "bonus"
    REFUND = "refund"

class Payout(BaseModel):
    __tablename__ = "payouts"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    currency = Column(String(3), default="USD")
    payout_type = Column(SQLEnum(PayoutType), nullable=False)
    status = Column(SQLEnum(PayoutStatus), default=PayoutStatus.PENDING)
    payment_method = Column(String(50))  # e.g., "bank_transfer", "paypal", "crypto"
    payment_details = Column(Text)  # JSON string with payment details
    reference_number = Column(String(100), unique=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    processed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<Payout(user_id='{self.user_id}', amount={self.amount}, status='{self.status}')>"