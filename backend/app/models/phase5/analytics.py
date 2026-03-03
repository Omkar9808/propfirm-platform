from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from datetime import datetime
from enum import Enum
import uuid

class TraderMetrics(BaseModel):
    __tablename__ = "trader_metrics"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    
    # Performance metrics
    total_accounts = Column(Numeric, default=0, nullable=False)
    active_accounts = Column(Numeric, default=0, nullable=False)
    passed_accounts = Column(Numeric, default=0, nullable=False)
    failed_accounts = Column(Numeric, default=0, nullable=False)
    
    # Trading metrics
    total_trades = Column(Numeric, default=0, nullable=False)
    winning_trades = Column(Numeric, default=0, nullable=False)
    losing_trades = Column(Numeric, default=0, nullable=False)
    total_profit = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    total_loss = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    total_commission = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    total_swap = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    
    # Risk metrics
    max_drawdown = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    avg_daily_loss = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    max_consecutive_losses = Column(Numeric, default=0, nullable=False)
    
    # Time-based metrics
    days_traded = Column(Numeric, default=0, nullable=False)
    avg_trades_per_day = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    last_trade_date = Column(DateTime(timezone=True))
    
    # Calculated metrics
    win_rate = Column(Numeric(precision=5, scale=2), default=0, nullable=False)  # Percentage
    profit_factor = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    sharpe_ratio = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    risk_reward_ratio = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    
    # Status and ranking
    is_active_trader = Column(Boolean, default=False, nullable=False)
    ranking_score = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    
    # Advanced scaling indicators
    tier_level = Column(Numeric, default=1, nullable=False)  # Current tier level
    tier_progress = Column(Numeric(precision=5, scale=2), default=0, nullable=False)  # Progress to next tier (0-100)
    scaling_multiplier = Column(Numeric(precision=5, scale=2), default=1.0, nullable=False)  # Current scaling multiplier
    max_tier_reached = Column(Numeric, default=1, nullable=False)  # Highest tier achieved
    
    # Advanced performance metrics
    consistency_score = Column(Numeric(precision=5, scale=2), default=0, nullable=False)  # Daily performance consistency
    risk_adjusted_return = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    volatility_score = Column(Numeric(precision=5, scale=2), default=0, nullable=False)
    
    # Momentum indicators
    performance_momentum = Column(Numeric(precision=5, scale=2), default=0, nullable=False)  # Recent performance trend
    streak_length = Column(Numeric, default=0, nullable=False)  # Current winning/losing streak
    streak_type = Column(String(20))  # "winning", "losing", or None
    
    # Advanced risk metrics
    value_at_risk = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    expected_shortfall = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    tail_risk = Column(Numeric(precision=5, scale=2), default=0, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="trader_metrics")
    
    def __repr__(self):
        return f"<TraderMetrics(user_id='{self.user_id}', win_rate={self.win_rate})>"

class LeaderboardPeriodEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"

class LeaderboardCache(BaseModel):
    __tablename__ = "leaderboard_cache"
    
    period = Column(String(20), nullable=False)  # daily, weekly, monthly, all_time
    rank = Column(Numeric, nullable=False)
    
    # Trader reference
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Cached metrics
    win_rate = Column(Numeric(precision=5, scale=2), nullable=False)
    total_profit = Column(Numeric(precision=12, scale=2), nullable=False)
    trades_count = Column(Numeric, nullable=False)
    ranking_score = Column(Numeric(precision=10, scale=2), nullable=False)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    # Unique constraint for one ranking per user per period
    __table_args__ = (
        Index('ix_leaderboard_cache_period_user_rank', 'period', 'user_id', 'rank', unique=True),
    )
    
    def __repr__(self):
        return f"<LeaderboardCache(period='{self.period}', rank={self.rank}, user_id='{self.user_id}')>"

class PlatformMetrics(BaseModel):
    __tablename__ = "platform_metrics"
    
    # Date for this metric snapshot
    metric_date = Column(DateTime(timezone=True), nullable=False, unique=True)
    
    # User metrics
    total_users = Column(Numeric, default=0, nullable=False)
    active_users = Column(Numeric, default=0, nullable=False)
    new_users = Column(Numeric, default=0, nullable=False)
    
    # Account metrics
    total_accounts = Column(Numeric, default=0, nullable=False)
    active_accounts = Column(Numeric, default=0, nullable=False)
    passed_accounts = Column(Numeric, default=0, nullable=False)
    failed_accounts = Column(Numeric, default=0, nullable=False)
    new_accounts = Column(Numeric, default=0, nullable=False)
    
    # Trading metrics
    total_trades = Column(Numeric, default=0, nullable=False)
    total_volume = Column(Numeric(precision=15, scale=2), default=0, nullable=False)
    total_revenue = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    
    # Financial metrics
    avg_account_balance = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    total_platform_equity = Column(Numeric(precision=15, scale=2), default=0, nullable=False)
    payout_ratio = Column(Numeric(precision=5, scale=2), default=0, nullable=False)  # Passed/Total accounts
    
    # Risk metrics
    avg_win_rate = Column(Numeric(precision=5, scale=2), default=0, nullable=False)
    platform_drawdown = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    
    # System metrics
    sync_success_rate = Column(Numeric(precision=5, scale=2), default=100, nullable=False)
    risk_evaluation_success_rate = Column(Numeric(precision=5, scale=2), default=100, nullable=False)
    
    def __repr__(self):
        return f"<PlatformMetrics(date='{self.metric_date}', total_users={self.total_users})>"

# Update User model to include trader metrics relationship
from app.models.user import User
User.trader_metrics = relationship("TraderMetrics", back_populates="user", uselist=False)

# Import Enum for LeaderboardPeriodEnum
from enum import Enum