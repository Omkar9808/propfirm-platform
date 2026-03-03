from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from enum import Enum

class CommissionTypeEnum(str, Enum):
    LIFETIME = "lifetime"
    ONE_TIME = "one_time"

class AffiliateTierEnum(str, Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    ELITE = "elite"
    ENTERPRISE = "enterprise"

# Affiliate Schemas
class AffiliateBase(BaseModel):
    tier: AffiliateTierEnum = AffiliateTierEnum.TIER_1
    commission_type: CommissionTypeEnum = CommissionTypeEnum.LIFETIME

class AffiliateCreate(AffiliateBase):
    user_id: UUID

class AffiliateUpdate(BaseModel):
    tier: Optional[AffiliateTierEnum] = None
    commission_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    commission_type: Optional[CommissionTypeEnum] = None
    is_active: Optional[bool] = None
    payout_threshold: Optional[Decimal] = Field(None, ge=0)

class AffiliateResponse(AffiliateBase):
    id: UUID
    user_id: UUID
    referral_code: str
    commission_percentage: Decimal
    is_active: bool
    total_referred_users: int
    total_revenue_generated: Decimal
    pending_commissions: Decimal
    paid_commissions: Decimal
    conversion_rate: Decimal
    average_revenue_per_user: Decimal
    payout_threshold: Decimal
    last_payout_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Referral Schemas
class ReferralBase(BaseModel):
    referral_code_used: str

class ReferralCreate(ReferralBase):
    referred_user_id: UUID

class ReferralResponse(ReferralBase):
    id: UUID
    affiliate_id: UUID
    referred_user_id: Optional[UUID] = None
    commission_percentage: Decimal
    commission_type: CommissionTypeEnum
    commission_amount: Decimal
    commission_paid: bool
    commission_paid_at: Optional[datetime] = None
    referred_user_registered_at: Optional[datetime] = None
    referred_user_first_purchase_at: Optional[datetime] = None
    referred_user_total_spent: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Commission Schemas
class AffiliateCommissionBase(BaseModel):
    amount: Decimal
    commission_type: str
    notes: Optional[str] = None

class AffiliateCommissionCreate(AffiliateCommissionBase):
    affiliate_id: UUID
    referral_id: UUID
    payment_id: Optional[UUID] = None

class AffiliateCommissionUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    processed_by: Optional[UUID] = None

class AffiliateCommissionResponse(AffiliateCommissionBase):
    id: UUID
    affiliate_id: UUID
    referral_id: UUID
    payment_id: Optional[UUID] = None
    status: str
    processed_at: Optional[datetime] = None
    processed_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Analytics Schemas
class AffiliateStatsResponse(BaseModel):
    affiliate_id: str
    referral_code: str
    tier: str
    commission_percentage: float
    commission_type: str
    is_active: bool
    total_referred_users: int
    total_revenue_generated: float
    pending_commissions: float
    paid_commissions: float
    conversion_rate: float
    average_revenue_per_user: float
    payout_threshold: float
    total_referrals: int
    paid_referrals: int
    pending_commissions_count: int
    paid_commissions_count: int
    last_payout_at: Optional[str] = None

class AffiliateDashboardResponse(BaseModel):
    affiliate: AffiliateResponse
    stats: AffiliateStatsResponse
    recent_commissions: List[AffiliateCommissionResponse]
    recent_referrals: List[ReferralResponse]

# Admin Schemas
class AdminAffiliateUpdate(BaseModel):
    tier: Optional[AffiliateTierEnum] = None
    commission_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    commission_type: Optional[CommissionTypeEnum] = None
    is_active: Optional[bool] = None
    payout_threshold: Optional[Decimal] = Field(None, ge=0)

class AffiliateListResponse(BaseModel):
    affiliates: List[AffiliateResponse]
    total_count: int
    page: int
    page_size: int