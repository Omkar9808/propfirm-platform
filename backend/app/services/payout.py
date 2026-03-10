from sqlalchemy.orm import Session
from app.models.payout import Payout, PayoutStatus, PayoutType
from app.models.user import User
from typing import List, Optional
from datetime import datetime
import uuid

class PayoutService:
    @staticmethod
    def create_payout(
        db: Session,
        user_id: uuid.UUID,
        amount: float,
        payout_type: PayoutType,
        payment_method: str,
        payment_details: str,
        notes: Optional[str] = None
    ) -> Payout:
        """Create a new payout request"""
        payout = Payout(
            user_id=user_id,
            amount=amount,
            payout_type=payout_type,
            payment_method=payment_method,
            payment_details=payment_details,
            reference_number=f"PAYOUT-{uuid.uuid4().hex[:8].upper()}",
            notes=notes
        )
        db.add(payout)
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def get_payout(db: Session, payout_id: uuid.UUID) -> Optional[Payout]:
        """Get a specific payout by ID"""
        return db.query(Payout).filter(Payout.id == payout_id).first()

    @staticmethod
    def get_user_payouts(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Payout]:
        """Get all payouts for a specific user"""
        return db.query(Payout).filter(Payout.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_pending_payouts(db: Session, skip: int = 0, limit: int = 100) -> List[Payout]:
        """Get all pending payouts for admin review"""
        return db.query(Payout).filter(Payout.status == PayoutStatus.PENDING).offset(skip).limit(limit).all()

    @staticmethod
    def approve_payout(db: Session, payout_id: uuid.UUID, approved_by: uuid.UUID) -> Optional[Payout]:
        """Approve a payout request"""
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout or payout.status != PayoutStatus.PENDING:
            return None
        
        payout.status = PayoutStatus.APPROVED
        payout.approved_by = approved_by
        payout.approved_at = datetime.utcnow()
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def reject_payout(db: Session, payout_id: uuid.UUID, notes: str) -> Optional[Payout]:
        """Reject a payout request"""
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout or payout.status != PayoutStatus.PENDING:
            return None
        
        payout.status = PayoutStatus.REJECTED
        payout.notes = notes
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def process_payout(db: Session, payout_id: uuid.UUID) -> Optional[Payout]:
        """Mark a payout as processing"""
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout or payout.status != PayoutStatus.APPROVED:
            return None
        
        payout.status = PayoutStatus.PROCESSING
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def complete_payout(db: Session, payout_id: uuid.UUID) -> Optional[Payout]:
        """Mark a payout as completed"""
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout or payout.status != PayoutStatus.PROCESSING:
            return None
        
        payout.status = PayoutStatus.COMPLETED
        payout.processed_at = datetime.utcnow()
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def cancel_payout(db: Session, payout_id: uuid.UUID) -> Optional[Payout]:
        """Cancel a payout request"""
        payout = db.query(Payout).filter(Payout.id == payout_id).first()
        if not payout or payout.status in [PayoutStatus.COMPLETED, PayoutStatus.CANCELLED]:
            return None
        
        payout.status = PayoutStatus.CANCELLED
        db.commit()
        db.refresh(payout)
        return payout

    @staticmethod
    def get_payout_stats(db: Session) -> dict:
        """Get payout statistics"""
        total_payouts = db.query(Payout).count()
        pending_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.PENDING).count()
        approved_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.APPROVED).count()
        processing_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.PROCESSING).count()
        completed_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.COMPLETED).count()
        rejected_payouts = db.query(Payout).filter(Payout.status == PayoutStatus.REJECTED).count()
        
        total_amount = db.query(Payout).filter(Payout.status == PayoutStatus.COMPLETED).with_entities(
            db.func.sum(Payout.amount)
        ).scalar() or 0
        
        return {
            "total_payouts": total_payouts,
            "pending_payouts": pending_payouts,
            "approved_payouts": approved_payouts,
            "processing_payouts": processing_payouts,
            "completed_payouts": completed_payouts,
            "rejected_payouts": rejected_payouts,
            "total_amount_paid": float(total_amount)
        }