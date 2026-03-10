from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, Enum as SQLEnum, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid

class CommissionTypeEnum(str, Enum):
    LIFETIME = "lifetime"
    ONE_TIME = "one_time"

class AffiliateTierEnum(str, Enum):
    TIER_1 = "tier_1"  # 20% direct referrals
    TIER_2 = "tier_2"  # 10% indirect referrals (2nd gen)
    TIER_3 = "tier_3"  # 5% 3rd generation referrals
    ELITE = "elite"    # 25% + performance bonuses
    ENTERPRISE = "enterprise"  # Custom structures

class Affiliate(BaseModel):
    """Enhanced affiliate system with tiered commissions"""
    __tablename__ = "affiliates"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    referral_code = Column(String(50), unique=True, nullable=False)
    tier = Column(SQLEnum(AffiliateTierEnum), default=AffiliateTierEnum.TIER_1, nullable=False)
    commission_percentage = Column(Numeric(precision=5, scale=2), default=20.00, nullable=False)
    commission_type = Column(SQLEnum(CommissionTypeEnum), default=CommissionTypeEnum.LIFETIME, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    total_referred_users = Column(Integer, default=0, nullable=False)
    total_revenue_generated = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    pending_commissions = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    paid_commissions = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    conversion_rate = Column(Numeric(precision=5, scale=2), default=0, nullable=False)
    average_revenue_per_user = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    payout_threshold = Column(Numeric(precision=10, scale=2), default=50.00, nullable=False)  # Minimum payout amount
    last_payout_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="affiliate")
    referrals = relationship("Referral", back_populates="affiliate")
    commission_records = relationship("AffiliateCommission", back_populates="affiliate")

class Referral(BaseModel):
    """Tracks individual referrals and their commission status"""
    __tablename__ = "referrals"
    
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id"), nullable=False)
    referred_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # NULL if user not registered yet
    referral_code_used = Column(String(50), nullable=False)  # The code that was used
    commission_percentage = Column(Numeric(precision=5, scale=2), nullable=False)
    commission_type = Column(SQLEnum(CommissionTypeEnum), nullable=False)
    commission_amount = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    commission_paid = Column(Boolean, default=False, nullable=False)
    commission_paid_at = Column(DateTime(timezone=True))
    referred_user_registered_at = Column(DateTime(timezone=True))
    referred_user_first_purchase_at = Column(DateTime(timezone=True))
    referred_user_total_spent = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    
    # Relationships
    affiliate = relationship("Affiliate", back_populates="referrals")
    referred_user = relationship("User", foreign_keys=[referred_user_id])

class AffiliateCommission(BaseModel):
    """Records actual commission payments to affiliates"""
    __tablename__ = "affiliate_commissions"
    
    affiliate_id = Column(UUID(as_uuid=True), ForeignKey("affiliates.id"), nullable=False)
    referral_id = Column(UUID(as_uuid=True), ForeignKey("referrals.id"), nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=True)  # Link to actual payment if exists
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    commission_type = Column(String(50), nullable=False)  # REGISTRATION, PURCHASE, RECURRING
    status = Column(String(20), default="pending", nullable=False)  # pending, paid, cancelled
    notes = Column(Text)
    processed_at = Column(DateTime(timezone=True))
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Admin who processed
    
    # Relationships
    affiliate = relationship("Affiliate", back_populates="commission_records")
    referral = relationship("Referral")
    payment = relationship("Payment")
    processed_by_user = relationship("User", foreign_keys=[processed_by])

# Update User model to include affiliate relationship
from app.models.user import User
User.affiliate = relationship("Affiliate", back_populates="user", uselist=False)