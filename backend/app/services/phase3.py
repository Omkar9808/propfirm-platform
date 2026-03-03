from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.phase3 import (
    TradeRepository, DailyStatRepository, 
    EquitySnapshotRepository, MT5SyncLogRepository
)
from app.repositories.phase2 import AccountRepository
from app.models.user import User
from app.models.phase2.account import Account
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import pytz
import time

class TradeService:
    """Service for trade processing and account balance updates"""
    
    @staticmethod
    def process_new_trade(db: Session, user: User, trade_data: dict) -> dict:
        """Process a new trade and update account balances"""
        account_id = trade_data['account_id']
        
        # Verify account ownership
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        if account.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this account"
            )
        
        # Verify account is active
        if account.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is not active"
            )
        
        try:
            # Create the trade
            trade = TradeRepository.create_trade(db, trade_data)
            
            # Update account balances if this is a closed trade
            if trade.status == "closed" and trade.close_time:
                TradeService._update_account_from_closed_trade(db, account, trade)
            
            # Create equity snapshot
            TradeService._create_equity_snapshot(db, account)
            
            return {
                "trade_id": trade.id,
                "ticket_id": trade.ticket_id,
                "status": "created",
                "account_balance": str(account.current_balance),
                "account_equity": str(account.equity)
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
    
    @staticmethod
    def update_trade(db: Session, user: User, trade_id: UUID, trade_data: dict) -> dict:
        """Update an existing trade and recalculate balances"""
        # Get trade and verify ownership
        trade = TradeRepository.get_trade_by_id(db, trade_id)
        if not trade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trade not found"
            )
        
        account = AccountRepository.get_account_by_id(db, trade.account_id)
        if account.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this trade"
            )
        
        # Update trade
        updated_trade = TradeRepository.update_trade(db, trade_id, trade_data)
        
        # If trade was closed, update account balances
        if updated_trade.status == "closed" and updated_trade.close_time:
            TradeService._update_account_from_closed_trade(db, account, updated_trade)
            TradeService._create_equity_snapshot(db, account)
        
        return {
            "trade_id": updated_trade.id,
            "status": "updated",
            "account_balance": str(account.current_balance),
            "account_equity": str(account.equity)
        }
    
    @staticmethod
    def get_account_trading_summary(db: Session, user: User, account_id: UUID) -> dict:
        """Get comprehensive trading summary for an account"""
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        if account.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this account"
            )
        
        summary = TradeRepository.get_account_trading_summary(db, account_id)
        summary["account_number"] = account.account_number
        
        return summary
    
    @staticmethod
    def _update_account_from_closed_trade(db: Session, account: Account, trade) -> None:
        """Update account balances based on closed trade results"""
        # Update current balance with profit/loss
        new_balance = account.current_balance + (trade.profit or Decimal('0'))
        new_equity = account.equity + (trade.profit or Decimal('0'))
        
        # Update with commissions and swaps
        if trade.commission:
            new_balance -= trade.commission
            new_equity -= trade.commission
        
        if trade.swap:
            new_balance += trade.swap
            new_equity += trade.swap
        
        # Update highest balance if new balance is higher
        highest_balance = max(new_balance, account.highest_balance)
        
        # Update account
        AccountRepository.update_account_balance(
            db, account.id, new_balance, new_equity, highest_balance
        )
    
    @staticmethod
    def _create_equity_snapshot(db: Session, account: Account) -> None:
        """Create an equity snapshot for the account"""
        EquitySnapshotRepository.create_snapshot(db, {
            "account_id": account.id,
            "timestamp": datetime.now(pytz.UTC),
            "balance": account.current_balance,
            "equity": account.equity,
            "margin": Decimal('0'),  # Would come from MT5
            "free_margin": Decimal('0'),  # Would come from MT5
            "margin_level": Decimal('0')  # Would come from MT5
        })

class MT5SyncService:
    """Service for MT5 synchronization and logging"""
    
    @staticmethod
    def sync_trades(db: Session, account_id: UUID, mt5_trades: list) -> dict:
        """Sync trades from MT5 to database"""
        start_time = time.time()
        
        # Verify account exists
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        sync_log_data = {
            "account_id": account_id,
            "sync_type": "trades",
            "status": "in_progress",
            "record_count": 0,
            "sync_started_at": datetime.now(pytz.UTC)
        }
        
        try:
            processed_count = 0
            for mt5_trade in mt5_trades:
                try:
                    # Check if trade already exists
                    existing_trade = TradeRepository.get_trade_by_ticket(
                        db, account_id, mt5_trade['ticket_id']
                    )
                    
                    if existing_trade:
                        # Update existing trade
                        TradeRepository.update_trade(db, existing_trade.id, mt5_trade)
                    else:
                        # Create new trade
                        mt5_trade['account_id'] = account_id
                        TradeRepository.create_trade(db, mt5_trade)
                    
                    processed_count += 1
                    
                except Exception as e:
                    # Log individual trade errors but continue processing
                    print(f"Error processing trade {mt5_trade.get('ticket_id')}: {e}")
                    continue
            
            # Update sync log with success
            sync_log_data.update({
                "status": "success",
                "record_count": processed_count,
                "sync_completed_at": datetime.now(pytz.UTC),
                "sync_duration_ms": int((time.time() - start_time) * 1000)
            })
            
            sync_log = MT5SyncLogRepository.create_sync_log(db, sync_log_data)
            
            # Update account equity snapshot after sync
            TradeService._create_equity_snapshot(db, account)
            
            return {
                "sync_id": sync_log.id,
                "status": "success",
                "processed_records": processed_count,
                "total_records": len(mt5_trades),
                "duration_ms": sync_log_data["sync_duration_ms"]
            }
            
        except Exception as e:
            # Update sync log with failure
            sync_log_data.update({
                "status": "failed",
                "error_message": str(e),
                "sync_completed_at": datetime.now(pytz.UTC),
                "sync_duration_ms": int((time.time() - start_time) * 1000)
            })
            
            sync_log = MT5SyncLogRepository.create_sync_log(db, sync_log_data)
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Sync failed: {str(e)}"
            )
    
    @staticmethod
    def sync_equity(db: Session, account_id: UUID, equity_data: dict) -> dict:
        """Sync equity data from MT5"""
        start_time = time.time()
        
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        sync_log_data = {
            "account_id": account_id,
            "sync_type": "equity",
            "status": "in_progress",
            "record_count": 1,
            "sync_started_at": datetime.now(pytz.UTC)
        }
        
        try:
            # Update account equity
            AccountRepository.update_account_balance(
                db, 
                account_id, 
                equity_data.get('balance', account.current_balance),
                equity_data.get('equity', account.equity)
            )
            
            # Create equity snapshot
            snapshot_data = {
                "account_id": account_id,
                "timestamp": datetime.now(pytz.UTC),
                "balance": equity_data.get('balance', account.current_balance),
                "equity": equity_data.get('equity', account.equity),
                "margin": equity_data.get('margin', Decimal('0')),
                "free_margin": equity_data.get('free_margin', Decimal('0')),
                "margin_level": equity_data.get('margin_level', Decimal('0'))
            }
            
            EquitySnapshotRepository.create_snapshot(db, snapshot_data)
            
            # Update sync log
            sync_log_data.update({
                "status": "success",
                "sync_completed_at": datetime.now(pytz.UTC),
                "sync_duration_ms": int((time.time() - start_time) * 1000)
            })
            
            sync_log = MT5SyncLogRepository.create_sync_log(db, sync_log_data)
            
            return {
                "sync_id": sync_log.id,
                "status": "success",
                "account_balance": str(account.current_balance),
                "account_equity": str(account.equity),
                "duration_ms": sync_log_data["sync_duration_ms"]
            }
            
        except Exception as e:
            sync_log_data.update({
                "status": "failed",
                "error_message": str(e),
                "sync_completed_at": datetime.now(pytz.UTC),
                "sync_duration_ms": int((time.time() - start_time) * 1000)
            })
            
            MT5SyncLogRepository.create_sync_log(db, sync_log_data)
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Equity sync failed: {str(e)}"
            )
    
    @staticmethod
    def get_sync_history(db: Session, user: User, account_id: UUID, limit: int = 50) -> list:
        """Get sync history for an account"""
        account = AccountRepository.get_account_by_id(db, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        if account.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this account"
            )
        
        sync_logs = MT5SyncLogRepository.get_sync_logs_by_account(db, account_id, limit)
        return [log.to_dict() for log in sync_logs]