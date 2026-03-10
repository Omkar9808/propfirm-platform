from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

# Trade schemas
class TradeBase(BaseModel):
    ticket_id: str = Field(..., max_length=50)
    symbol: str = Field(..., max_length=20)
    order_type: str = Field(..., max_length=10)  # BUY, SELL
    volume: Decimal = Field(..., gt=0)
    open_price: Decimal = Field(...)
    close_price: Optional[Decimal] = Field(None)
    stop_loss: Optional[Decimal] = Field(None)
    take_profit: Optional[Decimal] = Field(None)
    commission: Optional[Decimal] = Field(0)
    swap: Optional[Decimal] = Field(0)
    profit: Optional[Decimal] = Field(0)
    status: Optional[str] = Field("open", max_length=20)
    open_time: datetime
    close_time: Optional[datetime] = None
    comment: Optional[str] = Field(None, max_length=255)
    magic_number: Optional[int] = None

class TradeCreate(TradeBase):
    account_id: UUID

class TradeUpdate(BaseModel):
    close_price: Optional[Decimal] = Field(None)
    status: Optional[str] = Field(None, max_length=20)
    close_time: Optional[datetime] = None
    profit: Optional[Decimal] = Field(None)
    commission: Optional[Decimal] = Field(None)
    swap: Optional[Decimal] = Field(None)

class TradeResponse(TradeBase):
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Daily statistics schemas
class DailyStatBase(BaseModel):
    stat_date: datetime
    starting_balance: Decimal = Field(...)
    ending_balance: Optional[Decimal] = Field(None)
    daily_pnl: Optional[Decimal] = Field(0)
    total_commission: Optional[Decimal] = Field(0)
    total_swap: Optional[Decimal] = Field(0)
    trade_count: Optional[int] = 0
    winning_trades: Optional[int] = 0
    losing_trades: Optional[int] = 0
    max_drawdown: Optional[Decimal] = Field(0)

class DailyStatCreate(DailyStatBase):
    account_id: UUID

class DailyStatResponse(DailyStatBase):
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Equity snapshot schemas
class EquitySnapshotBase(BaseModel):
    timestamp: datetime
    balance: Decimal = Field(...)
    equity: Decimal = Field(...)
    margin: Optional[Decimal] = Field(0)
    free_margin: Optional[Decimal] = Field(0)
    margin_level: Optional[Decimal] = Field(0)

class EquitySnapshotCreate(EquitySnapshotBase):
    account_id: UUID

class EquitySnapshotResponse(EquitySnapshotBase):
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# MT5 sync log schemas
class MT5SyncLogBase(BaseModel):
    sync_type: str = Field(..., max_length=20)  # trades, equity, account_info
    status: str = Field(..., max_length=20)  # success, failed, partial
    record_count: Optional[int] = 0
    error_message: Optional[str] = None
    sync_duration_ms: Optional[int] = None
    sync_started_at: datetime
    sync_completed_at: Optional[datetime] = None
    mt5_server_time: Optional[datetime] = None

class MT5SyncLogCreate(MT5SyncLogBase):
    account_id: UUID

class MT5SyncLogResponse(MT5SyncLogBase):
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Trading data aggregation schemas
class AccountTradingSummary(BaseModel):
    account_id: UUID
    account_number: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: Optional[Decimal] = Field(None)
    total_profit: Decimal = Field(0)
    total_commission: Decimal = Field(0)
    total_swap: Decimal = Field(0)
    current_balance: Decimal = Field(0)
    current_equity: Decimal = Field(0)
    highest_balance: Decimal = Field(0)
    last_trade_time: Optional[datetime] = None
    last_sync_time: Optional[datetime] = None

class DailyPerformance(BaseModel):
    date: datetime
    starting_balance: Decimal = Field(0)
    ending_balance: Decimal = Field(0)
    daily_pnl: Decimal = Field(0)
    trade_count: int
    winning_trades: int
    losing_trades: int
    win_rate: Optional[Decimal] = Field(None)
    total_commission: Decimal = Field(0)
    total_swap: Decimal = Field(0)
    max_drawdown: Decimal = Field(0)