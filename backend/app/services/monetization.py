from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.monetization import (
    Affiliate, Referral, AffiliateCommission, 
    AffiliateTierEnum, CommissionTypeEnum
)
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase2.payment import Payment
from decimal import Decimal
import secrets
import string
from datetime import datetime, timezone

class AffiliateService:
    """Enhanced affiliate system service with tiered commissions"""
    
    @staticmethod
    def generate_referral_code(length: int = 8) -> str:
        """Generate unique referral code"""
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(characters) for _ in range(length))
            # Add prefix to make it more recognizable
            full_code = f"REF-{code}"
            # In production, check if code exists in database
            return full_code
    
    @staticmethod
    def create_affiliate(db: Session, user_id: str, tier: AffiliateTierEnum = AffiliateTierEnum.TIER_1) -> Affiliate:
        """Create affiliate account for user"""
        # Check if user already has affiliate account
        existing_affiliate = db.query(Affiliate).filter(Affiliate.user_id == user_id).first()
        if existing_affiliate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has an affiliate account"
            )
        
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Set commission percentage based on tier
        commission_percentage = AffiliateService._get_tier_commission(tier)
        
        affiliate = Affiliate(
            user_id=user_id,
            referral_code=AffiliateService.generate_referral_code(),
            tier=tier,
            commission_percentage=commission_percentage,
            commission_type=CommissionTypeEnum.LIFETIME
        )
        
        db.add(affiliate)
        db.commit()
        db.refresh(affiliate)
        return affiliate
    
    @staticmethod
    def _get_tier_commission(tier: AffiliateTierEnum) -> Decimal:
        """Get commission percentage for tier"""
        commission_map = {
            AffiliateTierEnum.TIER_1: Decimal('20.00'),
            AffiliateTierEnum.TIER_2: Decimal('10.00'),
            AffiliateTierEnum.TIER_3: Decimal('5.00'),
            AffiliateTierEnum.ELITE: Decimal('25.00'),
            AffiliateTierEnum.ENTERPRISE: Decimal('30.00')  # Custom, can be adjusted
        }
        return commission_map.get(tier, Decimal('20.00'))
    
    @staticmethod
    def track_referral(db: Session, referral_code: str, referred_user_id: str) -> Referral:
        """Track a new referral when user registers with referral code"""
        # Find affiliate by referral code
        affiliate = db.query(Affiliate).filter(
            Affiliate.referral_code == referral_code,
            Affiliate.is_active == True
        ).first()
        
        if not affiliate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid referral code"
            )
        
        # Check if user already exists (should not be possible in registration flow)
        existing_referral = db.query(Referral).filter(
            Referral.referred_user_id == referred_user_id
        ).first()
        
        if existing_referral:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already tracked as referral"
            )
        
        # Create referral record
        referral = Referral(
            affiliate_id=affiliate.id,
            referred_user_id=referred_user_id,
            referral_code_used=referral_code,
            commission_percentage=affiliate.commission_percentage,
            commission_type=affiliate.commission_type,
            referred_user_registered_at=datetime.now(timezone.utc)
        )
        
        db.add(referral)
        
        # Update affiliate stats
        affiliate.total_referred_users += 1
        db.commit()
        db.refresh(referral)
        return referral
    
    @staticmethod
    def calculate_commission(db: Session, referral_id: str, payment_amount: Decimal) -> Decimal:
        """Calculate commission amount for a referral"""
        referral = db.query(Referral).filter(Referral.id == referral_id).first()
        if not referral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referral not found"
            )
        
        if referral.commission_paid:
            return Decimal('0')
        
        # Calculate commission
        commission_amount = (payment_amount * referral.commission_percentage) / Decimal('100')
        return commission_amount
    
    @staticmethod
    def process_payment_commission(db: Session, payment_id: str) -> Optional[AffiliateCommission]:
        """Process commission when referred user makes a payment"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        # Find referral for this user
        referral = db.query(Referral).filter(
            Referral.referred_user_id == payment.user_id,
            Referral.commission_paid == False
        ).first()
        
        if not referral:
            # No referral found, no commission to process
            return None
        
        # Calculate commission
        commission_amount = AffiliateService.calculate_commission(db, str(referral.id), payment.amount)
        
        if commission_amount <= 0:
            return None
        
        # Create commission record
        commission = AffiliateCommission(
            affiliate_id=referral.affiliate_id,
            referral_id=referral.id,
            payment_id=payment_id,
            amount=commission_amount,
            commission_type="PURCHASE",
            status="pending"
        )
        
        db.add(commission)
        
        # Update referral
        referral.commission_amount = commission_amount
        referral.commission_paid = True
        referral.commission_paid_at = datetime.now(timezone.utc)
        referral.referred_user_first_purchase_at = datetime.now(timezone.utc)
        referral.referred_user_total_spent += payment.amount
        
        # Update affiliate stats
        affiliate = db.query(Affiliate).filter(Affiliate.id == referral.affiliate_id).first()
        if affiliate:
            affiliate.total_revenue_generated += payment.amount
            affiliate.pending_commissions += commission_amount
            affiliate.average_revenue_per_user = (
                affiliate.total_revenue_generated / affiliate.total_referred_users
                if affiliate.total_referred_users > 0 else Decimal('0')
            )
            affiliate.conversion_rate = (
                Decimal(affiliate.total_referred_users - affiliate.pending_commissions) / 
                affiliate.total_referred_users * Decimal('100')
                if affiliate.total_referred_users > 0 else Decimal('0')
            )
        
        db.commit()
        db.refresh(commission)
        return commission
    
    @staticmethod
    def get_affiliate_stats(db: Session, affiliate_id: str) -> dict:
        """Get comprehensive affiliate statistics"""
        affiliate = db.query(Affiliate).filter(Affiliate.id == affiliate_id).first()
        if not affiliate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Affiliate not found"
            )
        
        # Get referral statistics
        total_referrals = db.query(Referral).filter(
            Referral.affiliate_id == affiliate_id
        ).count()
        
        paid_referrals = db.query(Referral).filter(
            Referral.affiliate_id == affiliate_id,
            Referral.commission_paid == True
        ).count()
        
        pending_commissions_count = db.query(AffiliateCommission).filter(
            AffiliateCommission.affiliate_id == affiliate_id,
            AffiliateCommission.status == "pending"
        ).count()
        
        paid_commissions_count = db.query(AffiliateCommission).filter(
            AffiliateCommission.affiliate_id == affiliate_id,
            AffiliateCommission.status == "paid"
        ).count()
        
        return {
            "affiliate_id": str(affiliate.id),
            "referral_code": affiliate.referral_code,
            "tier": affiliate.tier.value,
            "commission_percentage": float(affiliate.commission_percentage),
            "commission_type": affiliate.commission_type.value,
            "is_active": affiliate.is_active,
            "total_referred_users": affiliate.total_referred_users,
            "total_revenue_generated": float(affiliate.total_revenue_generated),
            "pending_commissions": float(affiliate.pending_commissions),
            "paid_commissions": float(affiliate.paid_commissions),
            "conversion_rate": float(affiliate.conversion_rate),
            "average_revenue_per_user": float(affiliate.average_revenue_per_user),
            "payout_threshold": float(affiliate.payout_threshold),
            "total_referrals": total_referrals,
            "paid_referrals": paid_referrals,
            "pending_commissions_count": pending_commissions_count,
            "paid_commissions_count": paid_commissions_count,
            "last_payout_at": affiliate.last_payout_at.isoformat() if affiliate.last_payout_at else None
        }
    
    @staticmethod
    def update_affiliate_tier(db: Session, affiliate_id: str, new_tier: AffiliateTierEnum, 
                            new_commission_percentage: Optional[Decimal] = None) -> Affiliate:
        """Update affiliate tier and commission (admin function)"""
        affiliate = db.query(Affiliate).filter(Affiliate.id == affiliate_id).first()
        if not affiliate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Affiliate not found"
            )
        
        # Update tier
        affiliate.tier = new_tier
        
        # Update commission percentage
        if new_commission_percentage:
            affiliate.commission_percentage = new_commission_percentage
        else:
            affiliate.commission_percentage = AffiliateService._get_tier_commission(new_tier)
        
        db.commit()
        db.refresh(affiliate)
        return affiliate
    
    @staticmethod
    def get_pending_commissions(db: Session, affiliate_id: str) -> List[AffiliateCommission]:
        """Get all pending commissions for an affiliate"""
        return db.query(AffiliateCommission).filter(
            AffiliateCommission.affiliate_id == affiliate_id,
            AffiliateCommission.status == "pending"
        ).all()
    
    @staticmethod
    def get_affiliate_by_referral_code(db: Session, referral_code: str) -> Optional[Affiliate]:
        """Get affiliate by referral code"""
        return db.query(Affiliate).filter(
            Affiliate.referral_code == referral_code,
            Affiliate.is_active == True
        ).first()