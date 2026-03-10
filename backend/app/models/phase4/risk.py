from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import datetime
import uuid

class ViolationTypeEnum(str, Enum):
    DAILY_LOSS_EXCEEDED = "daily_loss_exceeded"
    TOTAL_LOSS_EXCEEDED = "total_loss_exceeded"
    MAX_POSITIONS_EXCEEDED = "max_positions_exceeded"
    UNAUTHORIZED_INSTRUMENT = "unauthorized_instrument"
    OUTSIDE_TRADING_HOURS = "outside_trading_hours"
    MAX_LOT_SIZE_EXCEEDED = "max_lot_size_exceeded"
    MANUAL_FAIL = "manual_fail"  # Admin override

class Violation(BaseModel):
    __tablename__ = "violations"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    violation_type = Column(SQLEnum(ViolationTypeEnum), nullable=False)
    description = Column(Text, nullable=False)
    
    # Violation details
    current_value = Column(Numeric(precision=12, scale=2))  # Current metric value
    threshold_value = Column(Numeric(precision=12, scale=2))  # Rule threshold
    symbol = Column(String(20))  # For instrument-specific violations
    trade_id = Column(UUID(as_uuid=True), ForeignKey("trades.id"))  # Related trade if applicable
    
    # Resolution status
    is_resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Admin who resolved
    resolution_notes = Column(Text)
    
    # Relationships
    account = relationship("Account", back_populates="violations")
    trade = relationship("Trade")
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<Violation(account_id='{self.account_id}', type='{self.violation_type}')>"

class AccountStatusEnum(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    FAILED = "failed"
    LOCKED = "locked"
    ARCHIVED = "archived"

class AccountStatusHistory(BaseModel):
    __tablename__ = "account_status_history"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    from_status = Column(SQLEnum(AccountStatusEnum))
    to_status = Column(SQLEnum(AccountStatusEnum), nullable=False)
    
    # Change details
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # System or admin
    change_reason = Column(Text, nullable=False)
    change_notes = Column(Text)
    
    # Violation reference (if status change due to violation)
    violation_id = Column(UUID(as_uuid=True), ForeignKey("violations.id"))
    
    # Timestamp
    changed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="status_history")
    changer = relationship("User", foreign_keys=[changed_by])
    violation = relationship("Violation")
    
    def __repr__(self):
        return f"<AccountStatusHistory(account_id='{self.account_id}', {self.from_status} → {self.to_status}')>"

class JobStatusEnum(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"

class JobExecutionLog(BaseModel):
    __tablename__ = "job_execution_log"
    
    job_name = Column(String(100), nullable=False)
    job_type = Column(String(50), nullable=False)  # risk_evaluation, sync, analytics
    status = Column(SQLEnum(JobStatusEnum), nullable=False)
    
    # Execution details
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Numeric)  # Execution duration in milliseconds
    
    # Processing metrics
    accounts_processed = Column(Numeric, default=0)
    accounts_passed = Column(Numeric, default=0)
    accounts_failed = Column(Numeric, default=0)
    violations_created = Column(Numeric, default=0)
    
    # Error handling
    error_message = Column(Text)
    stack_trace = Column(Text)  # For debugging
    
    # Metadata
    triggered_by = Column(String(50))  # system, manual, scheduled
    execution_context = Column(Text)  # JSON string with execution parameters
    
    def __repr__(self):
        return f"<JobExecutionLog(job='{self.job_name}', status='{self.status}')>"

# Update Account model to include new relationships
from app.models.phase2.account import Account
Account.violations = relationship("Violation", back_populates="account")
Account.status_history = relationship("AccountStatusHistory", back_populates="account")

# Update User model to handle resolver relationships
from app.models.user import User
User.resolved_violations = relationship("Violation", foreign_keys=[Violation.resolved_by])
User.status_changes = relationship("AccountStatusHistory", foreign_keys=[AccountStatusHistory.changed_by])