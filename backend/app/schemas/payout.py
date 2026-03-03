from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.payout import PayoutStatus, PayoutType

class PayoutCreate(BaseModel):
    amount: float
    payout_type: PayoutType
    payment_method: str
    payment_details: str
    notes: Optional[str] = None

class PayoutResponse(BaseModel):
    id: UUID
    user_id: UUID
    amount: float
    currency: str
    payout_type: PayoutType
    status: PayoutStatus
    payment_method: Optional[str]
    payment_details: Optional[str]
    reference_number: Optional[str]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    processed_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PayoutStats(BaseModel):
    total_payouts: int
    pending_payouts: int
    approved_payouts: int
    processing_payouts: int
    completed_payouts: int
    rejected_payouts: int
    total_amount_paid: float