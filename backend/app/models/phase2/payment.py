from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid

class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class PaymentMethodEnum(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
    SIMULATED = "simulated"  # For testing

class Payment(BaseModel):
    __tablename__ = "payments"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(SQLEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethodEnum), nullable=False)
    
    # Payment details
    transaction_id = Column(String(255), unique=True)  # External payment provider ID
    payment_intent_id = Column(String(255))  # For Stripe-like providers
    client_secret = Column(String(255))  # For frontend payment handling
    
    # Metadata
    payment_metadata = Column(Text)  # JSON string for additional payment data
    processed_at = Column(DateTime(timezone=True))
    failure_reason = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="payments", foreign_keys=[user_id])
    challenge = relationship("Challenge", back_populates="payments")
    revenue_entries = relationship("RevenueLedger", back_populates="payment")
    accounts = relationship("Account", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment(user_id='{self.user_id}', amount={self.amount}, status='{self.status}')>"

class RevenueTypeEnum(str, Enum):
    CHALLENGE_SALE = "challenge_sale"
    ACCOUNT_UPGRADE = "account_upgrade"
    REFUND = "refund"
    FEE = "fee"

class RevenueLedger(BaseModel):
    __tablename__ = "revenue_ledger"
    
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    revenue_type = Column(SQLEnum(RevenueTypeEnum), nullable=False)
    
    # Accounting fields
    is_processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    
    # Relationships
    payment = relationship("Payment", back_populates="revenue_entries")
    
    def __repr__(self):
        return f"<RevenueLedger(payment_id='{self.payment_id}', amount={self.amount}, type='{self.revenue_type}')>"