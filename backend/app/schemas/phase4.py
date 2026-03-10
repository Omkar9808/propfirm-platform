from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

# Violation schemas
class ViolationBase(BaseModel):
    violation_type: str = Field(..., max_length=50)
    description: str
    current_value: Optional[Decimal] = Field(None)
    threshold_value: Optional[Decimal] = Field(None)
    symbol: Optional[str] = Field(None, max_length=20)
    trade_id: Optional[UUID] = None

class ViolationCreate(ViolationBase):
    account_id: UUID

class ViolationUpdate(BaseModel):
    is_resolved: Optional[bool] = None
    resolution_notes: Optional[str] = None
    resolved_by: Optional[UUID] = None

class ViolationResponse(ViolationBase):
    id: UUID
    account_id: UUID
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Account status history schemas
class AccountStatusHistoryBase(BaseModel):
    from_status: Optional[str] = None
    to_status: str = Field(..., max_length=20)
    change_reason: str
    change_notes: Optional[str] = None
    violation_id: Optional[UUID] = None

class AccountStatusHistoryCreate(AccountStatusHistoryBase):
    account_id: UUID
    changed_by: Optional[UUID] = None

class AccountStatusHistoryResponse(AccountStatusHistoryBase):
    id: UUID
    account_id: UUID
    changed_by: Optional[UUID] = None
    changed_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Job execution log schemas
class JobExecutionLogBase(BaseModel):
    job_name: str = Field(..., max_length=100)
    job_type: str = Field(..., max_length=50)
    status: str = Field(..., max_length=20)
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    accounts_processed: Optional[int] = 0
    accounts_passed: Optional[int] = 0
    accounts_failed: Optional[int] = 0
    violations_created: Optional[int] = 0
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    triggered_by: Optional[str] = Field(None, max_length=50)
    execution_context: Optional[str] = None

class JobExecutionLogCreate(JobExecutionLogBase):
    pass

class JobExecutionLogResponse(JobExecutionLogBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Risk calculation schemas
class RiskMetrics(BaseModel):
    account_id: UUID
    account_number: str
    current_balance: Decimal = Field(0)
    current_equity: Decimal = Field(0)
    starting_balance: Decimal = Field(0)
    highest_balance: Decimal = Field(0)
    daily_start_balance: Decimal = Field(0)
    
    # Enhanced Drawdown Calculations
    daily_drawdown: Decimal = Field(0)
    daily_drawdown_percent: Decimal = Field(0)
    max_drawdown: Decimal = Field(0)
    max_drawdown_percent: Decimal = Field(0)
    trailing_drawdown: Decimal = Field(0)
    trailing_drawdown_percent: Decimal = Field(0)
    trailing_enabled: bool = False
    
    # Loss calculations
    total_loss: Decimal = Field(0)
    total_loss_percent: Decimal = Field(0)
    
    # Profit calculations
    profit: Decimal = Field(0)
    profit_percent: Decimal = Field(0)
    profit_target: Decimal = Field(0)
    profit_target_percent: Decimal = Field(0)
    
    # Position metrics
    open_positions: int = 0
    max_positions_allowed: int = 0
    largest_position: Decimal = Field(0)
    
    # Trade metrics
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: Decimal = Field(0)

class RuleViolation(BaseModel):
    violation_type: str
    description: str
    current_value: Decimal
    threshold_value: Decimal
    is_breached: bool

class RiskEvaluationResult(BaseModel):
    account_id: UUID
    account_number: str
    evaluation_time: datetime
    is_compliant: bool
    violations: List[RuleViolation]
    risk_metrics: RiskMetrics
    status_change: Optional[str] = None
    status_reason: Optional[str] = None

class AccountRiskStatus(BaseModel):
    account_id: UUID
    account_number: str
    current_status: str
    last_evaluation: Optional[datetime] = None
    active_violations: int
    total_violations: int
    days_active: int
    risk_score: Decimal = Field(0, )  # 0-100 scale

# Admin override schemas
class ManualAccountAction(BaseModel):
    account_id: UUID
    action: str = Field(..., max_length=20)  # pass, fail, lock, unlock
    reason: str = Field(..., max_length=500)
    notes: Optional[str] = None
    changed_by: Optional[UUID] = None

class RiskEngineSettings(BaseModel):
    evaluation_interval_minutes: int = Field(60, gt=0)
    max_daily_loss_percent: Decimal = Field(5.0, gt=0, le=100)
    max_total_loss_percent: Decimal = Field(10.0, gt=0, le=100)
    min_win_rate_percent: Decimal = Field(30.0, ge=0, le=100)
    is_enabled: bool = True
    last_evaluation_time: Optional[datetime] = None

class RiskEngineStatus(BaseModel):
    is_running: bool
    last_run_time: Optional[datetime] = None
    next_scheduled_run: Optional[datetime] = None
    accounts_evaluated: int
    accounts_passed: int
    accounts_failed: int
    violations_detected: int
    settings: RiskEngineSettings