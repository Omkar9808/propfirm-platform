from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID

# Challenge schemas
class ChallengeBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    is_featured: Optional[bool] = False
    sort_order: Optional[Decimal] = 0

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChallengeRuleVersionBase(BaseModel):
    version: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    max_daily_loss: Decimal = Field(..., gt=0)
    max_total_loss: Decimal = Field(..., gt=0)
    profit_target: Decimal = Field(..., gt=0)
    max_positions: int = Field(..., gt=0)
    max_lot_size: Decimal = Field(..., gt=0)
    allowed_instruments: Optional[str] = None  # JSON string
    trading_hours_start: Optional[str] = Field(None, pattern=r'^([01]\d|2[0-3]):[0-5]\d$')
    trading_hours_end: Optional[str] = Field(None, pattern=r'^([01]\d|2[0-3]):[0-5]\d$')
    is_active: Optional[bool] = True

class ChallengeRuleVersionCreate(ChallengeRuleVersionBase):
    challenge_id: UUID

class ChallengeRuleVersionResponse(ChallengeRuleVersionBase):
    id: UUID
    challenge_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Payment schemas
class PaymentBase(BaseModel):
    challenge_id: UUID
    amount: Decimal = Field(..., gt=0)
    currency: str = Field("USD", max_length=3)
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: UUID
    user_id: UUID
    status: str
    transaction_id: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RevenueLedgerBase(BaseModel):
    amount: Decimal = Field(...)
    currency: str = Field("USD", max_length=3)
    revenue_type: str

class RevenueLedgerCreate(RevenueLedgerBase):
    payment_id: UUID

class RevenueLedgerResponse(RevenueLedgerBase):
    id: UUID
    payment_id: UUID
    is_processed: bool
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Account schemas
class AccountBase(BaseModel):
    name: str = Field(..., max_length=100)
    starting_balance: Decimal = Field(..., gt=0)
    is_demo: Optional[bool] = True

class AccountCreate(AccountBase):
    payment_id: UUID

class AccountResponse(AccountBase):
    id: UUID
    user_id: UUID
    payment_id: UUID
    account_number: str
    status: str
    current_balance: Decimal
    daily_start_balance: Optional[Decimal] = None
    highest_balance: Decimal
    equity: Decimal
    activated_at: Optional[datetime] = None
    passed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AccountRuleSnapshotBase(BaseModel):
    max_daily_loss: Decimal = Field(...)
    max_total_loss: Decimal = Field(...)
    profit_target: Decimal = Field(...)
    max_positions: int
    max_lot_size: Decimal = Field(...)
    allowed_instruments: Optional[str] = None
    trading_hours_start: Optional[str] = None
    trading_hours_end: Optional[str] = None
    snapshot_version: str = Field(..., max_length=20)

class AccountRuleSnapshotCreate(AccountRuleSnapshotBase):
    account_id: UUID
    rule_version_id: UUID

class AccountRuleSnapshotResponse(AccountRuleSnapshotBase):
    id: UUID
    account_id: UUID
    rule_version_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True