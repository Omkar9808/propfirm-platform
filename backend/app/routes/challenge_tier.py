from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.challenge_tier import ChallengeTierService
from app.models.phase2.challenge import Challenge
from app.schemas.phase2 import ChallengeResponse
from app.schemas.challenge_tier import TierProgression, TierStatistics
from app.services.auth import AuthService
from app.models.user import User
from typing import List
import uuid

router = APIRouter()

@router.get("/tiers", response_model=List[ChallengeResponse])
def get_challenge_tiers(
    db: Session = Depends(get_db)
):
    """Get all challenges organized by tier level"""
    return ChallengeTierService.get_challenge_tiers(db)

@router.get("/tiers/{tier_level}", response_model=List[ChallengeResponse])
def get_tier_challenges(
    tier_level: int,
    db: Session = Depends(get_db)
):
    """Get all challenges for a specific tier level"""
    if tier_level < 1:
        raise HTTPException(status_code=400, detail="Tier level must be positive")
    return ChallengeTierService.get_tier_challenges(db, tier_level)

@router.get("/me/eligible", response_model=List[ChallengeResponse])
def get_my_eligible_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get challenges the current user is eligible for"""
    return ChallengeTierService.get_eligible_tiers(db, current_user.id)

@router.get("/me/progression", response_model=TierProgression)
def get_my_tier_progression(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get current user's tier progression status"""
    return ChallengeTierService.get_tier_progression(db, current_user.id)

@router.get("/statistics", response_model=TierStatistics)
def get_tier_statistics(
    db: Session = Depends(get_db)
):
    """Get statistics about challenge tiers"""
    return ChallengeTierService.get_tier_statistics(db)

@router.get("/rules/scaled/{challenge_id}")
def get_scaled_rules(
    challenge_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get scaled trading rules for a specific challenge"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Get base rules from the latest active rule version
    base_rules = challenge.rule_versions[0] if challenge.rule_versions else None
    if not base_rules:
        raise HTTPException(status_code=404, detail="No rule version found for this challenge")
    
    # Convert rule version to dictionary
    base_rules_dict = {
        "max_daily_loss": float(base_rules.max_daily_loss),
        "max_total_loss": float(base_rules.max_total_loss),
        "profit_target": float(base_rules.profit_target),
        "max_positions": int(base_rules.max_positions),
        "max_lot_size": float(base_rules.max_lot_size),
        "allowed_instruments": base_rules.allowed_instruments,
        "trading_hours_start": base_rules.trading_hours_start,
        "trading_hours_end": base_rules.trading_hours_end
    }
    
    scaled_rules = ChallengeTierService.calculate_scaled_rules(
        base_rules_dict, 
        challenge.multiplier
    )
    
    return {
        "challenge_id": challenge_id,
        "base_multiplier": float(challenge.multiplier),
        "base_rules": base_rules_dict,
        "scaled_rules": scaled_rules
    }