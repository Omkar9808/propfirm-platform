from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.schemas.phase2 import AccountResponse
from app.services.auth import AuthService
from app.services.phase2 import AccountService
from app.models.user import User

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=list[AccountResponse])
async def get_user_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all accounts for current user"""
    accounts = AccountService.get_user_accounts(db, current_user)
    return [AccountResponse.model_validate(account) for account in accounts]

@router.get("/{account_id}", response_model=dict)
async def get_account_details(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed account information including rule snapshot"""
    from uuid import UUID
    account_details = AccountService.get_account_details(db, current_user, UUID(account_id))
    return account_details

@router.post("/{account_id}/activate", response_model=dict)
async def activate_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Activate a pending account"""
    from uuid import UUID
    result = AccountService.activate_account(db, UUID(account_id))
    return result