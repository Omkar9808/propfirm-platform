from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from datetime import datetime
from enum import Enum
import uuid

class Trade(BaseModel):
    __tablename__ = "trades"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    ticket_id = Column(String(50), nullable=False)  # MT5 ticket ID - unique per account
    symbol = Column(String(20), nullable=False)
    order_type = Column(String(10), nullable=False)  # BUY, SELL
    volume = Column(Numeric(precision=10, scale=2), nullable=False)
    open_price = Column(Numeric(precision=12, scale=5), nullable=False)
    close_price = Column(Numeric(precision=12, scale=5))
    stop_loss = Column(Numeric(precision=12, scale=5))
    take_profit = Column(Numeric(precision=12, scale=5))
    commission = Column(Numeric(precision=10, scale=2), default=0)
    swap = Column(Numeric(precision=10, scale=2), default=0)
    profit = Column(Numeric(precision=12, scale=2), default=0)
    
    # Trade status
    status = Column(String(20), default="open")  # open, closed, cancelled
    open_time = Column(DateTime(timezone=True), nullable=False)
    close_time = Column(DateTime(timezone=True))
    
    # Metadata
    comment = Column(String(255))
    magic_number = Column(Numeric)  # MT5 magic number
    
    # Relationships
    account = relationship("Account", back_populates="trades")
    
    # Unique constraint to prevent duplicate trades
    __table_args__ = (
        Index('ix_trades_account_ticket', 'account_id', 'ticket_id', unique=True),
    )
    
    def __repr__(self):
        return f"<Trade(account_id='{self.account_id}', ticket_id='{self.ticket_id}', symbol='{self.symbol}')>"

class DailyStat(BaseModel):
    __tablename__ = "daily_stats"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    stat_date = Column(DateTime(timezone=True), nullable=False)
    
    # Daily metrics
    starting_balance = Column(Numeric(precision=12, scale=2), nullable=False)
    ending_balance = Column(Numeric(precision=12, scale=2))
    daily_pnl = Column(Numeric(precision=12, scale=2), default=0)
    total_commission = Column(Numeric(precision=10, scale=2), default=0)
    total_swap = Column(Numeric(precision=10, scale=2), default=0)
    trade_count = Column(Numeric, default=0)
    winning_trades = Column(Numeric, default=0)
    losing_trades = Column(Numeric, default=0)
    max_drawdown = Column(Numeric(precision=12, scale=2), default=0)
    
    # Relationships
    account = relationship("Account", back_populates="daily_stats")
    
    # Unique constraint for one stat per account per day
    __table_args__ = (
        Index('ix_daily_stats_account_date', 'account_id', 'stat_date', unique=True),
    )
    
    def __repr__(self):
        return f"<DailyStat(account_id='{self.account_id}', date='{self.stat_date}')>"

class EquitySnapshot(BaseModel):
    __tablename__ = "equity_snapshots"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    balance = Column(Numeric(precision=12, scale=2), nullable=False)
    equity = Column(Numeric(precision=12, scale=2), nullable=False)
    margin = Column(Numeric(precision=12, scale=2), default=0)
    free_margin = Column(Numeric(precision=12, scale=2), default=0)
    margin_level = Column(Numeric(precision=10, scale=2), default=0)
    
    # Relationships
    account = relationship("Account", back_populates="equity_snapshots")
    
    # Index for efficient time-based queries
    __table_args__ = (
        Index('ix_equity_snapshots_account_timestamp', 'account_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<EquitySnapshot(account_id='{self.account_id}', timestamp='{self.timestamp}')>"

class MT5SyncStatusEnum(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PARTIAL = "partial"

class MT5SyncLog(BaseModel):
    __tablename__ = "mt5_sync_log"
    
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    sync_type = Column(String(20), nullable=False)  # trades, equity, account_info
    status = Column(String(20), nullable=False)  # success, failed, partial
    record_count = Column(Numeric, default=0)
    error_message = Column(Text)
    sync_duration_ms = Column(Numeric)  # Duration in milliseconds
    
    # Sync metadata
    sync_started_at = Column(DateTime(timezone=True), nullable=False)
    sync_completed_at = Column(DateTime(timezone=True))
    mt5_server_time = Column(DateTime(timezone=True))  # MT5 server timestamp
    
    # Relationships
    account = relationship("Account", back_populates="mt5_sync_logs")
    
    def __repr__(self):
        return f"<MT5SyncLog(account_id='{self.account_id}', status='{self.status}', type='{self.sync_type}')>"

# Update Account model to include new relationships
from app.models.phase2.account import Account
Account.trades = relationship("Trade", back_populates="account")
Account.daily_stats = relationship("DailyStat", back_populates="account")
Account.equity_snapshots = relationship("EquitySnapshot", back_populates="account")
Account.mt5_sync_logs = relationship("MT5SyncLog", back_populates="account")

# Import Enum for MT5SyncStatusEnum
from enum import Enum