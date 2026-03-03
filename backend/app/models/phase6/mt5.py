from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, DateTime, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.models import BaseModel
from decimal import Decimal
from datetime import datetime
from enum import Enum
import uuid

class MT5ServerStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class MT5AccountStatusEnum(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SYNCING = "syncing"
    ERROR = "error"

class MT5TradeDirectionEnum(str, Enum):
    BUY = "buy"
    SELL = "sell"

class MT5TradeStatusEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELED = "canceled"

class MT5Server(BaseModel):
    __tablename__ = "mt5_servers"
    
    name = Column(String(100), nullable=False, unique=True)
    host = Column(String(100), nullable=False)
    port = Column(Numeric, nullable=False)
    status = Column(SQLEnum(MT5ServerStatusEnum), default=MT5ServerStatusEnum.ACTIVE, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    max_connections = Column(Numeric, default=100, nullable=False)
    current_connections = Column(Numeric, default=0, nullable=False)
    
    # Connection settings
    username = Column(String(100))  # For server authentication
    password = Column(String(100))  # For server authentication
    encryption_key = Column(Text)  # For secure communication
    
    # Metadata
    version = Column(String(20))
    description = Column(Text)
    last_heartbeat = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Relationships
    accounts = relationship("MT5Account", back_populates="server")
    
    def __repr__(self):
        return f"<MT5Server(name='{self.name}', host='{self.host}', status='{self.status}')>"

class MT5Account(BaseModel):
    __tablename__ = "mt5_accounts"
    
    # References
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    server_id = Column(UUID(as_uuid=True), ForeignKey("mt5_servers.id"), nullable=False)
    platform_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    
    # MT5 Account Information
    mt5_login = Column(String(50), nullable=False, unique=True)  # MT5 account number
    mt5_password = Column(String(100), nullable=False)  # Encrypted password
    mt5_investor_password = Column(String(100))  # Encrypted investor password
    currency = Column(String(3), default="USD", nullable=False)
    leverage = Column(Numeric, default=100, nullable=False)
    
    # Account Status
    status = Column(SQLEnum(MT5AccountStatusEnum), default=MT5AccountStatusEnum.DISCONNECTED, nullable=False)
    is_demo = Column(Boolean, default=True, nullable=False)
    is_master = Column(Boolean, default=False, nullable=False)  # Master account for copying
    
    # Balance Information
    balance = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    equity = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    margin = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    free_margin = Column(Numeric(precision=12, scale=2), default=0, nullable=False)
    margin_level = Column(Numeric(precision=10, scale=2), default=0, nullable=False)
    
    # Trading Information
    last_sync_time = Column(DateTime(timezone=True))
    next_sync_time = Column(DateTime(timezone=True))
    sync_interval_seconds = Column(Numeric, default=60, nullable=False)  # Sync every minute by default
    
    # Error handling
    error_count = Column(Numeric, default=0, nullable=False)
    last_error = Column(Text)
    last_error_time = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="mt5_accounts")
    server = relationship("MT5Server", back_populates="accounts")
    platform_account = relationship("Account", back_populates="mt5_account")
    trades = relationship("MT5Trade", back_populates="account")
    
    # Indexes
    __table_args__ = (
        Index('ix_mt5_accounts_user_server', 'user_id', 'server_id'),
        Index('ix_mt5_accounts_status', 'status'),
    )
    
    def __repr__(self):
        return f"<MT5Account(login='{self.mt5_login}', status='{self.status}')>"

class MT5Trade(BaseModel):
    __tablename__ = "mt5_trades"
    
    # References
    account_id = Column(UUID(as_uuid=True), ForeignKey("mt5_accounts.id"), nullable=False)
    platform_trade_id = Column(UUID(as_uuid=True), ForeignKey("trades.id"))  # Link to platform trade if exists
    
    # MT5 Trade Information
    mt5_ticket = Column(String(50), nullable=False)  # MT5 order ticket ID
    symbol = Column(String(20), nullable=False)
    direction = Column(SQLEnum(MT5TradeDirectionEnum), nullable=False)
    volume = Column(Numeric(precision=10, scale=2), nullable=False)
    price_open = Column(Numeric(precision=12, scale=5), nullable=False)
    price_close = Column(Numeric(precision=12, scale=5))
    
    # Timing
    time_open = Column(DateTime(timezone=True), nullable=False)
    time_close = Column(DateTime(timezone=True))
    time_update = Column(DateTime(timezone=True))
    
    # Trade Status
    status = Column(SQLEnum(MT5TradeStatusEnum), default=MT5TradeStatusEnum.OPEN, nullable=False)
    reason = Column(String(50))  # Reason for trade closure
    
    # Financial Information
    profit = Column(Numeric(precision=12, scale=2), default=0)
    swap = Column(Numeric(precision=12, scale=2), default=0)
    commission = Column(Numeric(precision=12, scale=2), default=0)
    sl = Column(Numeric(precision=12, scale=5))  # Stop Loss
    tp = Column(Numeric(precision=12, scale=5))  # Take Profit
    comment = Column(String(255))
    
    # Metadata
    magic_number = Column(Numeric)  # MT5 magic number for identification
    is_external = Column(Boolean, default=False, nullable=False)  # True if trade created outside platform
    
    # Relationships
    account = relationship("MT5Account", back_populates="trades")
    platform_trade = relationship("Trade", back_populates="mt5_trade")
    
    # Unique constraint for MT5 ticket per account
    __table_args__ = (
        Index('ix_mt5_trades_account_ticket', 'account_id', 'mt5_ticket', unique=True),
        Index('ix_mt5_trades_status_time', 'status', 'time_open'),
    )
    
    def __repr__(self):
        return f"<MT5Trade(ticket='{self.mt5_ticket}', symbol='{self.symbol}', status='{self.status}')>"

# Update existing models to include MT5 relationships
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase3.trading import Trade

User.mt5_accounts = relationship("MT5Account", back_populates="user")
Account.mt5_account = relationship("MT5Account", back_populates="platform_account", uselist=False)
Trade.mt5_trade = relationship("MT5Trade", back_populates="platform_trade", uselist=False)