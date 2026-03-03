from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.auth import AuthService
from app.models.user import User
from typing import Dict, List
from datetime import datetime, timedelta
from decimal import Decimal

# Create dependency functions
get_current_user = AuthService.get_current_user

router = APIRouter()

@router.get("/revenue-overview")
def get_revenue_overview(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get revenue overview for the specified period"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get revenue data from payments and revenue_ledger
    from app.models.phase2.payment import Payment
    from app.models.phase2.revenue_ledger import RevenueLedger
    
    # Total revenue
    total_revenue = db.query(RevenueLedger).filter(
        RevenueLedger.created_at >= start_date
    ).with_entities(
        db.func.sum(RevenueLedger.amount)
    ).scalar() or 0
    
    # Revenue by source
    challenge_revenue = db.query(RevenueLedger).filter(
        RevenueLedger.source_type == "challenge_fee",
        RevenueLedger.created_at >= start_date
    ).with_entities(
        db.func.sum(RevenueLedger.amount)
    ).scalar() or 0
    
    affiliate_revenue = db.query(RevenueLedger).filter(
        RevenueLedger.source_type == "affiliate_commission",
        RevenueLedger.created_at >= start_date
    ).with_entities(
        db.func.sum(RevenueLedger.amount)
    ).scalar() or 0
    
    # Revenue trend (daily breakdown)
    daily_revenue = []
    for i in range(days):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        day_revenue = db.query(RevenueLedger).filter(
            RevenueLedger.created_at >= day_start,
            RevenueLedger.created_at < day_end
        ).with_entities(
            db.func.sum(RevenueLedger.amount)
        ).scalar() or 0
        
        daily_revenue.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "revenue": float(day_revenue)
        })
    
    return {
        "period": {
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        "total_revenue": float(total_revenue),
        "revenue_by_source": {
            "challenge_fees": float(challenge_revenue),
            "affiliate_commissions": float(affiliate_revenue),
            "other": float(total_revenue - challenge_revenue - affiliate_revenue)
        },
        "daily_trend": daily_revenue,
        "average_daily_revenue": float(total_revenue / days) if days > 0 else 0
    }

@router.get("/affiliate-analytics")
def get_affiliate_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get affiliate program analytics"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get affiliate data
    from app.models.monetization import Affiliate
    
    # Total affiliates
    total_affiliates = db.query(Affiliate).count()
    
    # Active affiliates (with recent referrals)
    active_affiliates = db.query(Affiliate).filter(
        Affiliate.total_referrals > 0
    ).count()
    
    # Top performing affiliates
    top_affiliates = db.query(Affiliate).order_by(
        Affiliate.total_commissions.desc()
    ).limit(10).all()
    
    # Affiliate performance trend
    daily_affiliate_metrics = []
    for i in range(days):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        # New affiliates
        new_affiliates = db.query(Affiliate).filter(
            Affiliate.created_at >= day_start,
            Affiliate.created_at < day_end
        ).count()
        
        # New referrals
        new_referrals = db.query(Affiliate).filter(
            Affiliate.created_at >= day_start,
            Affiliate.created_at < day_end
        ).with_entities(
            db.func.sum(Affiliate.total_referrals)
        ).scalar() or 0
        
        daily_affiliate_metrics.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "new_affiliates": new_affiliates,
            "new_referrals": int(new_referrals)
        })
    
    return {
        "period": {
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        "affiliate_overview": {
            "total_affiliates": total_affiliates,
            "active_affiliates": active_affiliates,
            "conversion_rate": (active_affiliates / total_affiliates * 100) if total_affiliates > 0 else 0
        },
        "top_performers": [
            {
                "affiliate_id": str(affiliate.id),
                "referral_code": affiliate.referral_code,
                "total_referrals": affiliate.total_referrals,
                "total_commissions": float(affiliate.total_commissions),
                "tier_level": affiliate.tier_level
            }
            for affiliate in top_affiliates
        ],
        "daily_trend": daily_affiliate_metrics
    }

@router.get("/payout-analytics")
def get_payout_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payout system analytics"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get payout data
    from app.models.payout import Payout, PayoutStatus
    
    # Payout statistics
    total_payouts = db.query(Payout).count()
    pending_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.PENDING).count()
    approved_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.APPROVED).count()
    completed_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.COMPLETED).count()
    rejected_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.REJECTED).count()
    
    # Total amount paid
    total_paid = db.query(Payout).filter(
        Payout.status == PayoutStatus.COMPLETED
    ).with_entities(
        db.func.sum(Payout.amount)
    ).scalar() or 0
    
    # Payout trend
    daily_payout_metrics = []
    for i in range(days):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        # Payouts processed that day
        day_payouts = db.query(Payout).filter(
            Payout.processed_at >= day_start,
            Payout.processed_at < day_end,
            Payout.status == PayoutStatus.COMPLETED
        ).count()
        
        # Amount paid that day
        day_amount = db.query(Payout).filter(
            Payout.processed_at >= day_start,
            Payout.processed_at < day_end,
            Payout.status == PayoutStatus.COMPLETED
        ).with_entities(
            db.func.sum(Payout.amount)
        ).scalar() or 0
        
        daily_payout_metrics.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "payouts_processed": day_payouts,
            "amount_paid": float(day_amount)
        })
    
    return {
        "period": {
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        "payout_overview": {
            "total_payouts": total_payouts,
            "pending_payouts": pending_payouts,
            "approved_payouts": approved_payouts,
            "completed_payouts": completed_payouts,
            "rejected_payouts": rejected_payouts,
            "total_amount_paid": float(total_paid)
        },
        "payout_trend": daily_payout_metrics,
        "approval_rate": (completed_payouts / total_payouts * 100) if total_payouts > 0 else 0
    }

@router.get("/certificate-analytics")
def get_certificate_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get certificate system analytics"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get certificate data
    from app.models.certificate import Certificate
    
    # Certificate statistics
    total_certificates = db.query(Certificate).count()
    verified_certificates = db.query(Certificate).filter(Certificate.is_verified == True).count()
    unverified_certificates = db.query(Certificate).filter(Certificate.is_verified == False).count()
    
    # Certificate types breakdown
    certificate_types = db.query(
        Certificate.certificate_type,
        db.func.count(Certificate.id).label('count')
    ).group_by(Certificate.certificate_type).all()
    
    # Daily certificate issuance
    daily_certificates = []
    for i in range(days):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        day_issued = db.query(Certificate).filter(
            Certificate.created_at >= day_start,
            Certificate.created_at < day_end
        ).count()
        
        daily_certificates.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "certificates_issued": day_issued
        })
    
    return {
        "period": {
            "days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        "certificate_overview": {
            "total_certificates": total_certificates,
            "verified_certificates": verified_certificates,
            "unverified_certificates": unverified_certificates,
            "verification_rate": (verified_certificates / total_certificates * 100) if total_certificates > 0 else 0
        },
        "certificate_types": {
            cert_type: count for cert_type, count in certificate_types
        },
        "daily_issuance": daily_certificates
    }

@router.get("/monetization-dashboard")
def get_monetization_dashboard(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive monetization dashboard"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get all monetization data
    from app.routes.enhanced_metrics import get_revenue_overview
    from app.routes.enhanced_metrics import get_affiliate_analytics
    from app.routes.enhanced_metrics import get_payout_analytics
    from app.routes.enhanced_metrics import get_certificate_analytics
    
    # This would call the individual endpoints, but for now we'll return a combined structure
    return {
        "period": {
            "days": days,
            "start_date": (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d"),
            "end_date": datetime.utcnow().strftime("%Y-%m-%d")
        },
        "revenue_metrics": {
            "total_revenue": 0,
            "revenue_by_source": {},
            "daily_trend": []
        },
        "affiliate_metrics": {
            "total_affiliates": 0,
            "active_affiliates": 0,
            "top_performers": []
        },
        "payout_metrics": {
            "total_payouts": 0,
            "total_amount_paid": 0,
            "payout_trend": []
        },
        "certificate_metrics": {
            "total_certificates": 0,
            "verified_certificates": 0,
            "daily_issuance": []
        },
        "key_performance_indicators": {
            "revenue_growth_rate": 0,
            "affiliate_conversion_rate": 0,
            "payout_approval_rate": 0,
            "certificate_verification_rate": 0
        }
    }