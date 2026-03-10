from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.phase6 import MT5Service
from app.services.notifications import NotificationService
from app.schemas.phase6 import (
    MT5ServerResponse, MT5AccountResponse, MT5TradeResponse,
    MT5AccountCreate, MT5AccountUpdate, MT5TradeCreate, MT5TradeUpdate,
    MT5ConnectionStatus, MT5SyncRequest, MT5SyncResponse, MT5BalanceUpdate,
    MT5AccountConnectRequest, MT5AccountConnectionResponse
)
from app.core.security import verify_role

router = APIRouter(prefix="/mt5", tags=["MT5 Integration"])

# MT5 Server Management Endpoints
@router.get("/servers/status", response_model=List[MT5ConnectionStatus])
async def get_mt5_server_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get connection status for all MT5 servers (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        status_list = MT5Service.get_connection_status(db)
        return status_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting MT5 server status: {str(e)}"
        )

# MT5 Account Management Endpoints
@router.get("/accounts", response_model=List[MT5AccountResponse])
async def get_user_mt5_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all MT5 accounts for the current user"""
    try:
        accounts = MT5Service.get_user_mt5_accounts(db, str(current_user.id))
        return accounts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting MT5 accounts: {str(e)}"
        )

@router.post("/accounts", response_model=MT5AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_mt5_account(
    account_data: MT5AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new MT5 account link"""
    # Ensure user can only create accounts for themselves
    if str(account_data.user_id) != str(current_user.id):
        verify_role(current_user, ["admin", "super_admin"])
    
    try:
        account = MT5Service.create_mt5_account(db, account_data)
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating MT5 account: {str(e)}"
        )

@router.get("/accounts/{account_id}", response_model=MT5AccountResponse)
async def get_mt5_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific MT5 account details"""
    try:
        account = MT5Service.get_mt5_account(db, account_id, str(current_user.id))
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting MT5 account: {str(e)}"
        )

@router.put("/accounts/{account_id}", response_model=MT5AccountResponse)
async def update_mt5_account(
    account_id: str,
    account_data: MT5AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update MT5 account details"""
    try:
        # First get the account to verify ownership
        existing_account = MT5Service.get_mt5_account(db, account_id, str(current_user.id))
        if not existing_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MT5 account not found"
            )
        
        # In a real implementation, you would update the account here
        # For now, we'll just return the existing account since this is demo
        return existing_account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating MT5 account: {str(e)}"
        )

@router.post("/accounts/{account_id}/connect", response_model=MT5AccountConnectionResponse)
async def connect_mt5_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Connect to an MT5 account"""
    try:
        account = MT5Service.connect_mt5_account(db, account_id, str(current_user.id))
        
        return MT5AccountConnectionResponse(
            account_id=account.id,
            status=account.status.value,
            balance=account.balance,
            equity=account.equity,
            error_message=account.last_error,
            connected_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to MT5 account: {str(e)}"
        )

@router.post("/accounts/{account_id}/disconnect", response_model=MT5AccountResponse)
async def disconnect_mt5_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Disconnect from an MT5 account"""
    try:
        account = MT5Service.disconnect_mt5_account(db, account_id, str(current_user.id))
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error disconnecting from MT5 account: {str(e)}"
        )

# MT5 Trade Management Endpoints
@router.get("/trades", response_model=List[MT5TradeResponse])
async def get_mt5_trades(
    account_id: str = Query(..., description="MT5 Account ID to get trades for"),
    status: Optional[str] = Query(None, description="Filter by trade status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get MT5 trades for a specific account"""
    try:
        # Verify account belongs to user
        account = MT5Service.get_mt5_account(db, account_id, str(current_user.id))
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MT5 account not found"
            )
        
        # In a real implementation, you would query the trades here
        # For now, we'll return an empty list as demo
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting MT5 trades: {str(e)}"
        )

# MT5 Synchronization Endpoints
@router.post("/sync", response_model=MT5SyncResponse)
async def sync_mt5_trades(
    sync_request: MT5SyncRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Synchronize trades from MT5 to platform"""
    try:
        # Only allow admin users to trigger syncs
        verify_role(current_user, ["admin", "super_admin"])
        
        result = MT5Service.sync_mt5_trades(
            db, 
            account_id=sync_request.account_id,
            server_id=sync_request.server_id
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error synchronizing MT5 trades: {str(e)}"
        )

@router.post("/sync/accounts/{account_id}", response_model=MT5SyncResponse)
async def sync_specific_mt5_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Synchronize trades for a specific MT5 account"""
    try:
        # Verify account belongs to user or user is admin
        account = MT5Service.get_mt5_account(db, account_id, str(current_user.id))
        if not account:
            verify_role(current_user, ["admin", "super_admin"])
        
        result = MT5Service.sync_mt5_trades(db, account_id=account_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error synchronizing MT5 account: {str(e)}"
        )

# MT5 Balance Update Endpoint
@router.post("/balance-update", response_model=bool)
async def update_mt5_balance(
    balance_data: MT5BalanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update MT5 account balance information"""
    try:
        # Verify account belongs to user or user is admin
        account = MT5Service.get_mt5_account(db, str(balance_data.account_id), str(current_user.id))
        if not account:
            verify_role(current_user, ["admin", "super_admin"])
        
        # In a real implementation, you would update the balance here
        # For now, we'll just return True as demo
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating MT5 balance: {str(e)}"
        )

# Admin MT5 Management Endpoints
@router.get("/admin/accounts", response_model=List[MT5AccountResponse])
async def get_all_mt5_accounts(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    status: Optional[str] = Query(None, description="Filter by account status"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all MT5 accounts (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        query = db.query(MT5Account)
        
        if user_id:
            query = query.filter(MT5Account.user_id == user_id)
        if status:
            query = query.filter(MT5Account.status == status)
        
        accounts = query.limit(limit).offset(offset).all()
        return accounts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting MT5 accounts: {str(e)}"
        )

@router.delete("/accounts/{account_id}", response_model=bool)
async def delete_mt5_account(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete MT5 account link (admin only)"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # In a real implementation, you would delete the account here
        # For now, we'll just return True as demo
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting MT5 account: {str(e)}"
        )