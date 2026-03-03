from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.schemas.phase2 import (
    ChallengeCreate, ChallengeResponse,
    ChallengeRuleVersionCreate, ChallengeRuleVersionResponse,
    PaymentCreate, PaymentResponse,
    AccountResponse
)
from app.services.auth import AuthService
from app.services.phase2 import PaymentService, AccountService
from app.models.user import User

router = APIRouter(prefix="/challenges", tags=["challenges"])

# Challenge endpoints
@router.get("/challenges", response_model=list[ChallengeResponse])
async def get_challenges(
    db: Session = Depends(get_db)
):
    """Get all active challenges"""
    from app.repositories.phase2 import ChallengeRepository
    challenges = ChallengeRepository.get_active_challenges(db)
    return [ChallengeResponse.model_validate(challenge) for challenge in challenges]

@router.get("/challenges/featured", response_model=list[ChallengeResponse])
async def get_featured_challenges(
    db: Session = Depends(get_db)
):
    """Get featured challenges"""
    from app.repositories.phase2 import ChallengeRepository
    challenges = ChallengeRepository.get_featured_challenges(db)
    return [ChallengeResponse.model_validate(challenge) for challenge in challenges]

@router.post("/challenges", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge_data: ChallengeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new challenge (admin only)"""
    # Check if user is admin
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create challenges"
        )
    
    from app.repositories.phase2 import ChallengeRepository
    challenge = ChallengeRepository.create_challenge(db, challenge_data.model_dump())
    return ChallengeResponse.model_validate(challenge)

# Payment endpoints
@router.post("/payments", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new payment for challenge purchase"""
    result = PaymentService.create_payment(db, current_user, payment_data.model_dump())
    return result

@router.get("/payments", response_model=list)
async def get_user_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all payments for current user"""
    payments = PaymentService.get_user_payments(db, current_user)
    return payments

@router.post("/payments/{payment_id}/complete", response_model=dict)
async def complete_payment(
    payment_id: str,
    transaction_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Complete a payment (usually called by webhook)"""
    from uuid import UUID
    result = PaymentService.complete_payment(db, UUID(payment_id), transaction_id)
    return result


# Admin endpoints for challenge management
@router.get("/admin/challenges", response_model=list[ChallengeResponse])
async def admin_get_all_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all challenges (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    from app.repositories.phase2 import ChallengeRepository
    challenges = ChallengeRepository.get_active_challenges(db)
    return [ChallengeResponse.model_validate(challenge) for challenge in challenges]

@router.post("/admin/challenges/{challenge_id}/rules", 
            response_model=ChallengeRuleVersionResponse, 
            status_code=status.HTTP_201_CREATED)
async def create_challenge_rule_version(
    challenge_id: str,
    rule_data: ChallengeRuleVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new rule version for a challenge (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    from uuid import UUID
    from app.repositories.phase2 import ChallengeRuleVersionRepository
    rule_data_dict = rule_data.model_dump()
    rule_data_dict['challenge_id'] = UUID(challenge_id)
    
    rule_version = ChallengeRuleVersionRepository.create_rule_version(db, rule_data_dict)
    return ChallengeRuleVersionResponse.model_validate(rule_version)