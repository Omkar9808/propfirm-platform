from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

# Trader metrics schemas
class TraderMetricsBase(BaseModel):
    total_accounts: int = 0
    active_accounts: int = 0
    passed_accounts: int = 0
    failed_accounts: int = 0
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_profit: Decimal = Field(default=0)
    total_loss: Decimal = Field(default=0)
    total_commission: Decimal = Field(default=0)
    total_swap: Decimal = Field(default=0)
    max_drawdown: Decimal = Field(default=0)
    avg_daily_loss: Decimal = Field(default=0)
    max_consecutive_losses: int = 0
    days_traded: int = 0
    avg_trades_per_day: Decimal = Field(default=0)
    last_trade_date: Optional[datetime] = None
    win_rate: Decimal = Field(default=0)
    profit_factor: Decimal = Field(default=0)
    sharpe_ratio: Decimal = Field(default=0)
    risk_reward_ratio: Decimal = Field(default=0)
    is_active_trader: bool = False
    ranking_score: Decimal = Field(default=0)

class TraderMetricsCreate(TraderMetricsBase):
    user_id: UUID

class TraderMetricsUpdate(BaseModel):
    total_accounts: Optional[int] = None
    active_accounts: Optional[int] = None
    passed_accounts: Optional[int] = None
    failed_accounts: Optional[int] = None
    total_trades: Optional[int] = None
    winning_trades: Optional[int] = None
    losing_trades: Optional[int] = None
    total_profit: Optional[Decimal] = None
    total_loss: Optional[Decimal] = None
    total_commission: Optional[Decimal] = None
    total_swap: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None
    avg_daily_loss: Optional[Decimal] = None
    max_consecutive_losses: Optional[int] = None
    days_traded: Optional[int] = None
    avg_trades_per_day: Optional[Decimal] = None
    last_trade_date: Optional[datetime] = None
    win_rate: Optional[Decimal] = None
    profit_factor: Optional[Decimal] = None
    sharpe_ratio: Optional[Decimal] = None
    risk_reward_ratio: Optional[Decimal] = None
    is_active_trader: Optional[bool] = None
    ranking_score: Optional[Decimal] = None

class TraderMetricsResponse(TraderMetricsBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Leaderboard schemas
class LeaderboardEntry(BaseModel):
    rank: int
    user_id: UUID
    username: str
    win_rate: Decimal = Field(default=0)
    total_profit: Decimal = Field(default=0)
    trades_count: int
    ranking_score: Decimal = Field(default=0)
    period: str

class LeaderboardCacheBase(BaseModel):
    period: str = Field(..., max_length=20)
    rank: int
    user_id: UUID
    win_rate: Decimal = Field(...)
    total_profit: Decimal = Field(...)
    trades_count: int
    ranking_score: Decimal = Field(...)
    period_start: datetime
    period_end: datetime

class LeaderboardCacheCreate(LeaderboardCacheBase):
    pass

class LeaderboardCacheResponse(LeaderboardCacheBase):
    id: UUID
    calculated_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Platform metrics schemas
class PlatformMetricsBase(BaseModel):
    metric_date: datetime
    total_users: int = 0
    active_users: int = 0
    new_users: int = 0
    total_accounts: int = 0
    active_accounts: int = 0
    passed_accounts: int = 0
    failed_accounts: int = 0
    new_accounts: int = 0
    total_trades: int = 0
    total_volume: Decimal = Field(default=0)
    total_revenue: Decimal = Field(default=0)
    avg_account_balance: Decimal = Field(default=0)
    total_platform_equity: Decimal = Field(default=0)
    payout_ratio: Decimal = Field(default=0)
    avg_win_rate: Decimal = Field(default=0)
    platform_drawdown: Decimal = Field(default=0)
    sync_success_rate: Decimal = Field(default=100)
    risk_evaluation_success_rate: Decimal = Field(default=100)

class PlatformMetricsCreate(PlatformMetricsBase):
    pass

class PlatformMetricsResponse(PlatformMetricsBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Analytics aggregation schemas
class TraderPerformanceSummary(BaseModel):
    user_id: UUID
    username: str
    email: str
    trader_metrics: TraderMetricsResponse
    account_summary: dict
    recent_activity: dict

class PlatformOverview(BaseModel):
    total_users: int
    total_accounts: int
    active_accounts: int
    passed_accounts: int
    failed_accounts: int
    total_trades: int
    total_revenue: Decimal = Field(default=0)
    avg_win_rate: Decimal = Field(default=0)
    payout_ratio: Decimal = Field(default=0)
    last_updated: datetime

class AnalyticsSettings(BaseModel):
    leaderboard_update_interval_minutes: int = Field(60, gt=0)
    metrics_calculation_interval_minutes: int = Field(30, gt=0)
    data_retention_days: int = Field(365, gt=0)
    is_leaderboard_enabled: bool = True
    is_platform_metrics_enabled: bool = True

class AnalyticsStatus(BaseModel):
    is_running: bool
    last_metrics_calculation: Optional[datetime] = None
    last_leaderboard_update: Optional[datetime] = None
    next_scheduled_run: Optional[datetime] = None
    traders_processed: int
    leaderboard_entries: int
    platform_metrics_entries: int
    settings: AnalyticsSettings

# Admin dashboard schemas
class AdminDashboardMetrics(BaseModel):
    user_metrics: dict
    account_metrics: dict
    trading_metrics: dict
    financial_metrics: dict
    system_metrics: dict
    recent_activity: List[dict]

class UserManagementAction(BaseModel):
    user_id: UUID
    action: str = Field(..., max_length=20)  # suspend, unsuspend, delete, reset_password
    reason: str = Field(..., max_length=500)
    notes: Optional[str] = None
    performed_by: Optional[UUID] = None

class AccountManagementAction(BaseModel):
    account_id: UUID
    action: str = Field(..., max_length=20)  # review, reset, recalculate
    reason: str = Field(..., max_length=500)
    notes: Optional[str] = None
    performed_by: Optional[UUID] = None

class RevenueReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    group_by: str = Field("day", max_length=10)  # day, week, month
    include_details: bool = True

class RevenueReportResponse(BaseModel):
    period: str
    total_revenue: Decimal = Field(default=0)
    new_revenue: Decimal = Field(0)
    processed_revenue: Decimal = Field(0)
    refund_amount: Decimal = Field(0)
    net_revenue: Decimal = Field(0)
    transaction_count: int
    details: Optional[List[dict]] = None