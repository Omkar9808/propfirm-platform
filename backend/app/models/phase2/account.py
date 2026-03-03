from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid

class AccountStatusEnum(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    LOCKED = "locked"
    ARCHIVED = "archived"

class Account(BaseModel):
    __tablename__ = "accounts"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Challenge Account #12345"
    account_number = Column(String(50), unique=True, nullable=False)  # Unique identifier
    status = Column(SQLEnum(AccountStatusEnum), default=AccountStatusEnum.PENDING, nullable=False)
    
    # Account balances
    starting_balance = Column(Numeric(precision=12, scale=2), nullable=False)
    current_balance = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    daily_start_balance = Column(Numeric(precision=12, scale=2))  # For daily loss calculation
    highest_balance = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    equity = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    
    # Account metadata
    mt5_login = Column(String(50))  # MT5 account login (will be populated later)
    mt5_password = Column(String(100))  # MT5 account password (encrypted)
    server = Column(String(100))  # MT5 server name
    is_demo = Column(Boolean, default=True, nullable=False)  # Demo vs Live account
    
    # Lock information
    locked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Admin who locked
    locked_reason = Column(Text)  # Reason for locking
    locked_at = Column(DateTime(timezone=True))
    
    # Timestamps
    activated_at = Column(DateTime(timezone=True))
    passed_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    last_evaluated_at = Column(DateTime(timezone=True))  # For race condition protection
    
    # Relationships
    user = relationship("User", back_populates="accounts", foreign_keys=[user_id])
    payment = relationship("Payment", back_populates="accounts")
    rule_snapshot = relationship("AccountRuleSnapshot", back_populates="account", uselist=False)
    trades = relationship("Trade", back_populates="account")
    daily_stats = relationship("DailyStat", back_populates="account")
    equity_snapshots = relationship("EquitySnapshot", back_populates="account")
    violations = relationship("Violation", back_populates="account")
    status_history = relationship("AccountStatusHistory", back_populates="account")
    
    def __repr__(self):
        return f"<Account(account_number='{self.account_number}', status='{self.status}')>"

class AccountRuleSnapshot(BaseModel):
    __tablename__ = "account_rule_snapshots"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, unique=True)
    rule_version_id = Column(UUID(as_uuid=True), ForeignKey("challenge_rule_versions.id"), nullable=False)
    
    # Snapshotted rules (copied from challenge_rule_versions at account creation)
    max_daily_loss = Column(Numeric(precision=10, scale=2), nullable=False)
    max_total_loss = Column(Numeric(precision=10, scale=2), nullable=False)
    profit_target = Column(Numeric(precision=10, scale=2), nullable=False)
    max_positions = Column(Numeric, nullable=False)
    max_lot_size = Column(Numeric(precision=10, scale=2), nullable=False)
    allowed_instruments = Column(Text)  # JSON string
    trading_hours_start = Column(String(5))
    trading_hours_end = Column(String(5))
    
    # Metadata
    snapshot_version = Column(String(20), nullable=False)  # Version when snapshot was taken
    notes = Column(Text)
    
    # Relationships
    account = relationship("Account", back_populates="rule_snapshot")
    rule_version = relationship("ChallengeRuleVersion", back_populates="account_snapshots")
    
    def __repr__(self):
        return f"<AccountRuleSnapshot(account_id='{self.account_id}', version='{self.snapshot_version}')>"

# Update User model to include relationships
from app.models.user import User
User.payments = relationship("Payment", back_populates="user", foreign_keys="Payment.user_id")
User.accounts = relationship("Account", back_populates="user", foreign_keys="Account.user_id")