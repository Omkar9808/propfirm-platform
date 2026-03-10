from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.payout import PayoutService
from app.models.payout import Payout, PayoutStatus, PayoutType
from app.schemas.payout import PayoutCreate, PayoutResponse, PayoutStats
from app.services.auth import AuthService
from app.models.user import User
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=PayoutResponse)
def create_payout(
    payout_data: PayoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Create a new payout request"""
    payout = PayoutService.create_payout(
        db=db,
        user_id=current_user.id,
        amount=payout_data.amount,
        payout_type=payout_data.payout_type,
        payment_method=payout_data.payment_method,
        payment_details=payout_data.payment_details,
        notes=payout_data.notes
    )
    return payout

@router.get("/me", response_model=List[PayoutResponse])
def get_my_payouts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get all payouts for the current user"""
    return PayoutService.get_user_payouts(db, current_user.id, skip, limit)

@router.get("/{payout_id}", response_model=PayoutResponse)
def get_payout(
    payout_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get a specific payout by ID"""
    payout = PayoutService.get_payout(db, payout_id)
    if not payout:
        raise HTTPException(status_code=404, detail="Payout not found")
    if payout.user_id != current_user.id and current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to view this payout")
    return payout

@router.get("/admin/pending", response_model=List[PayoutResponse])
def get_pending_payouts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get all pending payouts for admin review"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return PayoutService.get_pending_payouts(db, skip, limit)

@router.post("/{payout_id}/approve")
def approve_payout(
    payout_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Approve a payout request"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payout = PayoutService.approve_payout(db, payout_id, current_user.id)
    if not payout:
        raise HTTPException(status_code=400, detail="Cannot approve this payout")
    return {"message": "Payout approved successfully"}

@router.post("/{payout_id}/reject")
def reject_payout(
    payout_id: uuid.UUID,
    notes: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Reject a payout request"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payout = PayoutService.reject_payout(db, payout_id, notes)
    if not payout:
        raise HTTPException(status_code=400, detail="Cannot reject this payout")
    return {"message": "Payout rejected successfully"}

@router.post("/{payout_id}/process")
def process_payout(
    payout_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Mark a payout as processing"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payout = PayoutService.process_payout(db, payout_id)
    if not payout:
        raise HTTPException(status_code=400, detail="Cannot process this payout")
    return {"message": "Payout marked as processing"}

@router.post("/{payout_id}/complete")
def complete_payout(
    payout_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Mark a payout as completed"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    payout = PayoutService.complete_payout(db, payout_id)
    if not payout:
        raise HTTPException(status_code=400, detail="Cannot complete this payout")
    return {"message": "Payout completed successfully"}

@router.post("/{payout_id}/cancel")
def cancel_payout(
    payout_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Cancel a payout request"""
    payout = PayoutService.get_payout(db, payout_id)
    if not payout:
        raise HTTPException(status_code=404, detail="Payout not found")
    
    # Users can cancel their own pending payouts, admins can cancel any
    if payout.user_id != current_user.id and current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to cancel this payout")
    
    payout = PayoutService.cancel_payout(db, payout_id)
    if not payout:
        raise HTTPException(status_code=400, detail="Cannot cancel this payout")
    return {"message": "Payout cancelled successfully"}

@router.get("/admin/stats", response_model=PayoutStats)
def get_payout_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get payout statistics"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return PayoutService.get_payout_stats(db)