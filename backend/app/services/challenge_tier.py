from sqlalchemy.orm import Session
from app.models.phase2.challenge import Challenge
from typing import List, Optional
from decimal import Decimal
import uuid

class ChallengeTierService:
    @staticmethod
    def get_challenge_tiers(db: Session) -> List[Challenge]:
        """Get all challenges organized by tier level"""
        return db.query(Challenge).filter(
            Challenge.status == "active"
        ).order_by(Challenge.tier_level, Challenge.sort_order).all()

    @staticmethod
    def get_tier_challenges(db: Session, tier_level: int) -> List[Challenge]:
        """Get all challenges for a specific tier level"""
        return db.query(Challenge).filter(
            Challenge.tier_level == tier_level,
            Challenge.status == "active"
        ).order_by(Challenge.sort_order).all()

    @staticmethod
    def get_eligible_tiers(db: Session, user_id: uuid.UUID) -> List[Challenge]:
        """Get challenges the user is eligible for based on their progress"""
        # Get all completed challenges for this user
        from app.models.phase2.account import Account
        from app.models.phase2.account_status_history import AccountStatusHistory
        
        completed_challenges = db.query(Account.challenge_id).join(
            AccountStatusHistory, Account.id == AccountStatusHistory.account_id
        ).filter(
            Account.user_id == user_id,
            AccountStatusHistory.new_status == "PASSED"
        ).distinct().all()
        
        completed_challenge_ids = [ch[0] for ch in completed_challenges]
        
        # Get challenges where user has completed the prerequisite (if any)
        eligible_challenges = db.query(Challenge).filter(
            Challenge.status == "active"
        ).filter(
            (Challenge.prerequisite_challenge_id == None) |
            (Challenge.prerequisite_challenge_id.in_(completed_challenge_ids))
        ).order_by(Challenge.tier_level, Challenge.sort_order).all()
        
        return eligible_challenges

    @staticmethod
    def get_tier_progression(db: Session, user_id: uuid.UUID) -> dict:
        """Get user's tier progression status"""
        # Get user's highest completed tier
        from app.models.phase2.account import Account
        from app.models.phase2.account_status_history import AccountStatusHistory
        
        highest_tier = db.query(
            db.func.max(Challenge.tier_level)
        ).join(Account, Challenge.id == Account.challenge_id).join(
            AccountStatusHistory, Account.id == AccountStatusHistory.account_id
        ).filter(
            Account.user_id == user_id,
            AccountStatusHistory.new_status == "PASSED"
        ).scalar() or 0
        
        # Get next available tier
        next_tier = int(highest_tier) + 1 if highest_tier is not None else 1
        
        # Get challenges in next tier that user is eligible for
        next_tier_challenges = ChallengeTierService.get_tier_challenges(db, next_tier)
        eligible_next_tier = []
        
        for challenge in next_tier_challenges:
            if challenge.prerequisite_challenge_id is None:
                eligible_next_tier.append(challenge)
            else:
                # Check if user completed the prerequisite
                prerequisite_completed = db.query(AccountStatusHistory).join(
                    Account, Account.id == AccountStatusHistory.account_id
                ).filter(
                    Account.user_id == user_id,
                    Account.challenge_id == challenge.prerequisite_challenge_id,
                    AccountStatusHistory.new_status == "PASSED"
                ).first()
                
                if prerequisite_completed:
                    eligible_next_tier.append(challenge)
        
        return {
            "current_tier": int(highest_tier),
            "next_tier": next_tier,
            "eligible_challenges": eligible_next_tier,
            "total_tiers": db.query(db.func.max(Challenge.tier_level)).filter(
                Challenge.status == "active"
            ).scalar() or 0
        }

    @staticmethod
    def calculate_scaled_rules(base_rules: dict, multiplier: Decimal) -> dict:
        """Calculate scaled trading rules based on multiplier"""
        scaled_rules = base_rules.copy()
        
        # Scale monetary values
        monetary_fields = ['max_daily_loss', 'max_total_loss', 'profit_target']
        for field in monetary_fields:
            if field in scaled_rules:
                scaled_rules[field] = float(Decimal(str(scaled_rules[field])) * multiplier)
        
        # Scale position limits (usually increased)
        if 'max_positions' in scaled_rules:
            scaled_rules['max_positions'] = int(Decimal(str(scaled_rules['max_positions'])) * multiplier)
        
        # Scale lot sizes (usually increased)
        if 'max_lot_size' in scaled_rules:
            scaled_rules['max_lot_size'] = float(Decimal(str(scaled_rules['max_lot_size'])) * multiplier)
        
        return scaled_rules

    @staticmethod
    def get_tier_statistics(db: Session) -> dict:
        """Get statistics about challenge tiers"""
        total_tiers = db.query(db.func.max(Challenge.tier_level)).filter(
            Challenge.status == "active"
        ).scalar() or 0
        
        tier_stats = {}
        for tier in range(1, int(total_tiers) + 1):
            challenge_count = db.query(Challenge).filter(
                Challenge.tier_level == tier,
                Challenge.status == "active"
            ).count()
            
            avg_price = db.query(db.func.avg(Challenge.price)).filter(
                Challenge.tier_level == tier,
                Challenge.status == "active"
            ).scalar() or 0
            
            tier_stats[f"tier_{tier}"] = {
                "challenge_count": challenge_count,
                "average_price": float(avg_price),
                "multiplier_range": db.query(
                    db.func.min(Challenge.multiplier),
                    db.func.max(Challenge.multiplier)
                ).filter(
                    Challenge.tier_level == tier,
                    Challenge.status == "active"
                ).first()
            }
        
        return {
            "total_tiers": int(total_tiers),
            "tier_statistics": tier_stats
        }