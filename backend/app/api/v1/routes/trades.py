from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.schemas.phase3 import (
    TradeCreate, TradeUpdate, TradeResponse,
    DailyStatCreate, DailyStatResponse,
    EquitySnapshotCreate, EquitySnapshotResponse,
    MT5SyncLogCreate, MT5SyncLogResponse,
    AccountTradingSummary, DailyPerformance
)
from app.services.auth import AuthService
from app.services.phase3 import TradeService, MT5SyncService
from app.models.user import User
from typing import List
from datetime import date
from uuid import UUID

router = APIRouter(prefix="/trades", tags=["trades"])

# Trade endpoints
@router.post("/trades", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade_data: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new trade for an account"""
    result = TradeService.process_new_trade(db, current_user, trade_data.model_dump())
    return result

@router.put("/trades/{trade_id}", response_model=dict)
async def update_trade(
    trade_id: str,
    trade_data: TradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing trade"""
    from uuid import UUID
    result = TradeService.update_trade(db, current_user, UUID(trade_id), trade_data.model_dump(exclude_unset=True))
    return result

@router.get("/trades/account/{account_id}", response_model=List[TradeResponse])
async def get_account_trades(
    account_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all trades for a specific account"""
    from uuid import UUID
    from app.repositories.phase3 import TradeRepository
    
    trades = TradeRepository.get_trades_by_account(db, UUID(account_id), skip, limit)
    return [TradeResponse.model_validate(trade) for trade in trades]

@router.get("/trades/account/{account_id}/summary", response_model=AccountTradingSummary)
async def get_account_trading_summary(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive trading summary for an account"""
    from uuid import UUID
    summary = TradeService.get_account_trading_summary(db, current_user, UUID(account_id))
    return AccountTradingSummary(**summary)

# Daily statistics endpoints
@router.post("/daily-stats", response_model=DailyStatResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_stat(
    stat_data: DailyStatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create or update daily statistics for an account"""
    from app.repositories.phase3 import DailyStatRepository
    from uuid import UUID
    
    # Verify account ownership
    from app.repositories.phase2 import AccountRepository
    account = AccountRepository.get_account_by_id(db, UUID(stat_data.account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    stat = DailyStatRepository.create_daily_stat(db, stat_data.model_dump())
    return DailyStatResponse.model_validate(stat)

@router.get("/daily-stats/account/{account_id}", response_model=List[DailyStatResponse])
async def get_account_daily_stats(
    account_id: str,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get daily statistics for an account"""
    from uuid import UUID
    from app.repositories.phase3 import DailyStatRepository
    
    stats = DailyStatRepository.get_daily_stats_by_account(db, UUID(account_id), days)
    return [DailyStatResponse.model_validate(stat) for stat in stats]

@router.post("/daily-stats/account/{account_id}/calculate", response_model=DailyStatResponse)
async def calculate_daily_stats(
    account_id: str,
    stat_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calculate and store daily statistics for a specific date"""
    from uuid import UUID
    from app.repositories.phase3 import DailyStatRepository
    
    # Verify account ownership
    from app.repositories.phase2 import AccountRepository
    account = AccountRepository.get_account_by_id(db, UUID(account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    # Calculate stats
    calculated_stats = DailyStatRepository.calculate_daily_stats(db, UUID(account_id), stat_date)
    stat = DailyStatRepository.create_daily_stat(db, calculated_stats)
    return DailyStatResponse.model_validate(stat)

# Equity snapshot endpoints
@router.post("/equity-snapshots", response_model=EquitySnapshotResponse, status_code=status.HTTP_201_CREATED)
async def create_equity_snapshot(
    snapshot_data: EquitySnapshotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new equity snapshot"""
    from app.repositories.phase3 import EquitySnapshotRepository
    from uuid import UUID
    
    # Verify account ownership
    from app.repositories.phase2 import AccountRepository
    account = AccountRepository.get_account_by_id(db, UUID(snapshot_data.account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    snapshot = EquitySnapshotRepository.create_snapshot(db, snapshot_data.model_dump())
    return EquitySnapshotResponse.model_validate(snapshot)

@router.get("/equity-snapshots/account/{account_id}", response_model=List[EquitySnapshotResponse])
async def get_account_equity_snapshots(
    account_id: str,
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get equity snapshots for an account"""
    from uuid import UUID
    from app.repositories.phase3 import EquitySnapshotRepository
    
    snapshots = EquitySnapshotRepository.get_snapshots_by_account(db, UUID(account_id), hours)
    return [EquitySnapshotResponse.model_validate(snapshot) for snapshot in snapshots]

# MT5 sync endpoints
@router.post("/mt5-sync/trades/{account_id}", response_model=dict)
async def sync_mt5_trades(
    account_id: str,
    mt5_trades: List[dict],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Sync trades from MT5 to database"""
    from uuid import UUID
    result = MT5SyncService.sync_trades(db, UUID(account_id), mt5_trades)
    return result

@router.post("/mt5-sync/equity/{account_id}", response_model=dict)
async def sync_mt5_equity(
    account_id: str,
    equity_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Sync equity data from MT5"""
    from uuid import UUID
    result = MT5SyncService.sync_equity(db, UUID(account_id), equity_data)
    return result

@router.get("/mt5-sync/history/{account_id}", response_model=List[dict])
async def get_sync_history(
    account_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get MT5 sync history for an account"""
    from uuid import UUID
    history = MT5SyncService.get_sync_history(db, current_user, UUID(account_id), limit)
    return history

@router.get("/mt5-sync/status/{account_id}", response_model=dict)
async def get_recent_sync_status(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get the most recent sync status for an account"""
    from uuid import UUID
    from app.repositories.phase3 import MT5SyncLogRepository
    
    # Verify account ownership
    from app.repositories.phase2 import AccountRepository
    account = AccountRepository.get_account_by_id(db, UUID(account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    recent_sync = MT5SyncLogRepository.get_recent_sync_status(db, UUID(account_id))
    if recent_sync:
        return recent_sync.to_dict()
    else:
        return {"status": "no_sync_history"}

# Admin endpoints for monitoring
@router.get("/admin/trading-overview", response_model=dict)
async def get_trading_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get overall trading platform statistics (admin only)"""
    # Check admin privileges
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    from app.repositories.phase3 import TradeRepository
    from app.repositories.phase2 import AccountRepository
    
    # Get platform-wide statistics
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(Account.status == "active").count()
    
    # This would need more complex queries for real statistics
    return {
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "total_trades": 0,  # Would need aggregation
        "total_volume": 0,  # Would need aggregation
        "platform_equity": 0  # Would need aggregation
    }