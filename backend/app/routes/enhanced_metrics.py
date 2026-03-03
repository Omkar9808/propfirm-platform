from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.enhanced_metrics import EnhancedTraderMetricsService
from app.services.auth import AuthService
from app.models.user import User
from typing import Dict

router = APIRouter()

@router.get("/me/scaling-indicators")
def get_my_scaling_indicators(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get advanced scaling indicators for current user"""
    scaling_data = EnhancedTraderMetricsService.calculate_scaling_indicators(
        db, current_user.id
    )
    return scaling_data

@router.get("/me/scaling-profile")
def get_my_scaling_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get complete trader scaling profile"""
    profile = EnhancedTraderMetricsService.get_trader_scaling_profile(
        db, current_user.id
    )
    return profile

@router.post("/me/update-scaling")
def update_my_scaling_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Update trader metrics with advanced scaling indicators"""
    updated_metrics = EnhancedTraderMetricsService.update_trader_metrics_with_scaling(
        db, current_user.id
    )
    if not updated_metrics:
        raise HTTPException(status_code=404, detail="Trader metrics not found")
    return {"message": "Scaling metrics updated successfully", "metrics": updated_metrics}

@router.get("/me/tier-requirements")
def get_tier_requirements():
    """Get requirements for each tier level"""
    return {
        "tier_1": {
            "name": "Beginner",
            "requirements": {
                "passed_accounts": 1,
                "min_win_rate": 50,
                "min_profit_factor": 1.0
            },
            "multiplier": 1.0,
            "benefits": ["Basic trading access", "Standard account sizes"]
        },
        "tier_2": {
            "name": "Intermediate",
            "requirements": {
                "passed_accounts": 3,
                "min_win_rate": 55,
                "min_profit_factor": 1.2
            },
            "multiplier": 1.5,
            "benefits": ["Increased account sizes", "Enhanced trading tools", "Priority support"]
        },
        "tier_3": {
            "name": "Advanced",
            "requirements": {
                "passed_accounts": 5,
                "min_win_rate": 60,
                "min_profit_factor": 1.5
            },
            "multiplier": 2.0,
            "benefits": ["Large account sizes", "Advanced analytics", "Dedicated account manager"]
        },
        "tier_4": {
            "name": "Elite",
            "requirements": {
                "passed_accounts": 10,
                "min_win_rate": 65,
                "min_profit_factor": 2.0
            },
            "multiplier": 3.0,
            "benefits": ["Maximum account sizes", "Premium features", "VIP support", "Exclusive opportunities"]
        }
    }

@router.get("/me/scaling-progress")
def get_scaling_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get detailed progress toward next tier"""
    # Get current metrics
    from app.models.phase5.analytics import TraderMetrics
    trader_metrics = db.query(TraderMetrics).filter(
        TraderMetrics.user_id == current_user.id
    ).first()
    
    if not trader_metrics:
        raise HTTPException(status_code=404, detail="Trader metrics not found")
    
    # Calculate current tier and progress
    current_tier = int(trader_metrics.tier_level)
    tier_progress = float(trader_metrics.tier_progress)
    
    # Get requirements for next tier
    tier_requirements = {
        1: {"passed_accounts": 1, "win_rate": 50, "profit_factor": 1.0},
        2: {"passed_accounts": 3, "win_rate": 55, "profit_factor": 1.2},
        3: {"passed_accounts": 5, "win_rate": 60, "profit_factor": 1.5},
        4: {"passed_accounts": 10, "win_rate": 65, "profit_factor": 2.0}
    }
    
    next_tier = current_tier + 1 if current_tier < 4 else 4
    req = tier_requirements.get(next_tier, {})
    
    # Calculate individual metric progress
    progress_details = {}
    if req:
        progress_details = {
            "passed_accounts": {
                "current": int(trader_metrics.passed_accounts),
                "required": req["passed_accounts"],
                "progress": min(100, (float(trader_metrics.passed_accounts) / req["passed_accounts"]) * 100)
            },
            "win_rate": {
                "current": float(trader_metrics.win_rate),
                "required": req["win_rate"],
                "progress": min(100, (float(trader_metrics.win_rate) / req["win_rate"]) * 100)
            },
            "profit_factor": {
                "current": float(trader_metrics.profit_factor),
                "required": req["profit_factor"],
                "progress": min(100, (float(trader_metrics.profit_factor) / req["profit_factor"]) * 100)
            }
        }
    
    return {
        "current_tier": current_tier,
        "next_tier": next_tier,
        "overall_progress": tier_progress,
        "progress_details": progress_details,
        "scaling_multiplier": float(trader_metrics.scaling_multiplier)
    }