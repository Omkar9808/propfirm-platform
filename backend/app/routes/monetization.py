from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.services.auth import AuthService

# Create dependency functions
get_current_user = AuthService.get_current_user
get_current_active_user = AuthService.get_current_active_user
from app.services.monetization import AffiliateService
from app.schemas.monetization import (
    AffiliateCreate, AffiliateUpdate, AffiliateResponse,
    ReferralCreate, ReferralResponse,
    AffiliateCommissionResponse, AffiliateCommissionUpdate,
    AffiliateStatsResponse, AffiliateDashboardResponse,
    AdminAffiliateUpdate, AffiliateListResponse
)
from app.models.user import User
from app.models.monetization import AffiliateTierEnum
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# User Affiliate Endpoints
@router.post("/affiliate", response_model=AffiliateResponse, status_code=status.HTTP_201_CREATED)
def create_affiliate_account(
    affiliate_data: AffiliateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create affiliate account for current user"""
    # Verify user is creating affiliate for themselves
    if str(affiliate_data.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only create affiliate account for yourself"
        )
    
    try:
        affiliate = AffiliateService.create_affiliate(
            db, str(current_user.id), affiliate_data.tier
        )
        return affiliate
    except Exception as e:
        logger.error(f"Error creating affiliate account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/affiliate/me", response_model=AffiliateResponse)
def get_my_affiliate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's affiliate account"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    return affiliate

@router.get("/affiliate/dashboard", response_model=AffiliateDashboardResponse)
def get_affiliate_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive affiliate dashboard"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    
    # Get stats
    stats = AffiliateService.get_affiliate_stats(db, str(affiliate.id))
    
    # Get recent commissions (last 10)
    recent_commissions = db.query(AffiliateCommissionResponse).filter(
        AffiliateCommissionResponse.affiliate_id == affiliate.id
    ).order_by(AffiliateCommissionResponse.created_at.desc()).limit(10).all()
    
    # Get recent referrals (last 10)
    recent_referrals = db.query(ReferralResponse).filter(
        ReferralResponse.affiliate_id == affiliate.id
    ).order_by(ReferralResponse.created_at.desc()).limit(10).all()
    
    return {
        "affiliate": affiliate,
        "stats": stats,
        "recent_commissions": recent_commissions,
        "recent_referrals": recent_referrals
    }

@router.put("/affiliate/me", response_model=AffiliateResponse)
def update_affiliate_account(
    update_data: AffiliateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user's affiliate account"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    
    # Only allow user to update certain fields
    updatable_fields = ["commission_type"]
    for field in updatable_fields:
        if hasattr(update_data, field) and getattr(update_data, field) is not None:
            setattr(affiliate, field, getattr(update_data, field))
    
    db.commit()
    db.refresh(affiliate)
    return affiliate

@router.get("/affiliate/stats", response_model=AffiliateStatsResponse)
def get_affiliate_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get affiliate statistics"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    
    return AffiliateService.get_affiliate_stats(db, str(affiliate.id))

@router.get("/affiliate/commissions/pending", response_model=List[AffiliateCommissionResponse])
def get_pending_commissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pending commissions for current affiliate"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    
    commissions = AffiliateService.get_pending_commissions(db, str(affiliate.id))
    return commissions

# Referral Endpoints
@router.post("/referrals", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
def track_referral(
    referral_data: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Track a new referral (typically called during user registration)"""
    try:
        referral = AffiliateService.track_referral(
            db, referral_data.referral_code_used, str(current_user.id)
        )
        return referral
    except Exception as e:
        logger.error(f"Error tracking referral: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/referrals/me", response_model=List[ReferralResponse])
def get_my_referrals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get referrals made by current user"""
    affiliate = current_user.affiliate
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate account not found"
        )
    
    referrals = db.query(ReferralResponse).filter(
        ReferralResponse.affiliate_id == affiliate.id
    ).offset(skip).limit(limit).all()
    
    return referrals

# Public Endpoints
@router.get("/referral-codes/{referral_code}/validate")
def validate_referral_code(referral_code: str, db: Session = Depends(get_db)):
    """Validate if referral code exists and is active"""
    affiliate = AffiliateService.get_affiliate_by_referral_code(db, referral_code)
    if not affiliate:
        return {"valid": False, "message": "Invalid or inactive referral code"}
    
    return {
        "valid": True,
        "affiliate_id": str(affiliate.id),
        "tier": affiliate.tier.value,
        "commission_percentage": float(affiliate.commission_percentage)
    }

# Admin Endpoints
@router.get("/admin/affiliates", response_model=AffiliateListResponse)
def list_affiliates(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    tier: str = Query(None),
    is_active: bool = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin: List all affiliates with filtering"""
    # Check admin permissions
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    query = db.query(AffiliateResponse)
    
    if tier:
        query = query.filter(AffiliateResponse.tier == tier)
    if is_active is not None:
        query = query.filter(AffiliateResponse.is_active == is_active)
    
    total_count = query.count()
    affiliates = query.offset(skip).limit(limit).all()
    
    return {
        "affiliates": affiliates,
        "total_count": total_count,
        "page": skip // limit + 1,
        "page_size": limit
    }

@router.get("/admin/affiliates/{affiliate_id}", response_model=AffiliateDashboardResponse)
def get_affiliate_details(
    affiliate_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin: Get detailed affiliate information"""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    affiliate = db.query(AffiliateResponse).filter(AffiliateResponse.id == affiliate_id).first()
    if not affiliate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Affiliate not found"
        )
    
    stats = AffiliateService.get_affiliate_stats(db, str(affiliate_id))
    
    # Get all commissions
    all_commissions = db.query(AffiliateCommissionResponse).filter(
        AffiliateCommissionResponse.affiliate_id == affiliate_id
    ).order_by(AffiliateCommissionResponse.created_at.desc()).all()
    
    # Get all referrals
    all_referrals = db.query(ReferralResponse).filter(
        ReferralResponse.affiliate_id == affiliate_id
    ).order_by(ReferralResponse.created_at.desc()).all()
    
    return {
        "affiliate": affiliate,
        "stats": stats,
        "recent_commissions": all_commissions,
        "recent_referrals": all_referrals
    }

@router.put("/admin/affiliates/{affiliate_id}", response_model=AffiliateResponse)
def update_affiliate(
    affiliate_id: UUID,
    update_data: AdminAffiliateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin: Update affiliate account"""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    try:
        affiliate = AffiliateService.update_affiliate_tier(
            db, 
            str(affiliate_id), 
            update_data.tier or AffiliateTierEnum.TIER_1,
            update_data.commission_percentage
        )
        return affiliate
    except Exception as e:
        logger.error(f"Error updating affiliate: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/admin/affiliates/{affiliate_id}/commissions/{commission_id}/process")
def process_commission(
    affiliate_id: UUID,
    commission_id: UUID,
    update_data: AffiliateCommissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin: Process (approve/pay) affiliate commission"""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    commission = db.query(AffiliateCommissionResponse).filter(
        AffiliateCommissionResponse.id == commission_id,
        AffiliateCommissionResponse.affiliate_id == affiliate_id
    ).first()
    
    if not commission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )
    
    # Update commission status
    if update_data.status:
        commission.status = update_data.status
    if update_data.notes:
        commission.notes = update_data.notes
    commission.processed_by = current_user.id
    commission.processed_at = datetime.utcnow()
    
    # Update affiliate pending/paid amounts
    affiliate = db.query(AffiliateResponse).filter(AffiliateResponse.id == affiliate_id).first()
    if affiliate and commission.status == "paid":
        affiliate.pending_commissions -= commission.amount
        affiliate.paid_commissions += commission.amount
        affiliate.last_payout_at = datetime.utcnow()
    
    db.commit()
    db.refresh(commission)
    
    return {"message": "Commission processed successfully", "commission": commission}