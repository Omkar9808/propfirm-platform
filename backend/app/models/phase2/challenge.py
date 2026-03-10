from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from enum import Enum
import uuid

class ChallengeStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class Challenge(BaseModel):
    __tablename__ = "challenges"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(precision=10, scale=2), nullable=False)  # e.g., 99.99
    status = Column(SQLEnum(ChallengeStatusEnum), default=ChallengeStatusEnum.ACTIVE, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Numeric, default=0, nullable=False)
    tier_level = Column(Numeric, default=1, nullable=False)  # 1, 2, 3, etc.
    multiplier = Column(Numeric(precision=5, scale=2), default=1.0, nullable=False)  # Scaling multiplier
    prerequisite_challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=True)  # For tier progression
    
    # Relationships
    rule_versions = relationship("ChallengeRuleVersion", back_populates="challenge")
    payments = relationship("Payment", back_populates="challenge")
    prerequisite_challenge = relationship("Challenge", remote_side="Challenge.id", uselist=False)
    
    def __repr__(self):
        return f"<Challenge(name='{self.name}', price={self.price})>"

class ChallengeRuleVersion(BaseModel):
    __tablename__ = "challenge_rule_versions"
    
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    version = Column(String(20), nullable=False)  # e.g., "1.0", "2.1"
    name = Column(String(100), nullable=False)  # e.g., "Standard Rules v1.0"
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Trading Rules
    max_daily_loss = Column(Numeric(precision=10, scale=2), nullable=False)  # e.g., 500.00
    max_total_loss = Column(Numeric(precision=10, scale=2), nullable=False)  # e.g., 1000.00
    profit_target = Column(Numeric(precision=10, scale=2), nullable=False)   # e.g., 2000.00
    max_positions = Column(Numeric, nullable=False)  # e.g., 5
    max_lot_size = Column(Numeric(precision=10, scale=2), nullable=False)    # e.g., 1.0
    allowed_instruments = Column(Text)  # JSON string of allowed instruments
    trading_hours_start = Column(String(5))  # e.g., "00:00"
    trading_hours_end = Column(String(5))    # e.g., "23:59"
    
    # Relationships
    challenge = relationship("Challenge", back_populates="rule_versions")
    account_snapshots = relationship("AccountRuleSnapshot", back_populates="rule_version")
    
    def __repr__(self):
        return f"<ChallengeRuleVersion(challenge_id='{self.challenge_id}', version='{self.version}')>"