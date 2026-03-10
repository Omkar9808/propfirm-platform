from sqlalchemy.orm import Session
from app.models.phase3.trading import Trade, DailyStat, EquitySnapshot, MT5SyncLog
from app.models.phase2.account import Account
from uuid import UUID
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, date
import pytz

class TradeRepository:
    """Repository for trade-related database operations"""
    
    @staticmethod
    def get_trade_by_id(db: Session, trade_id: UUID) -> Optional[Trade]:
        return db.query(Trade).filter(Trade.id == trade_id).first()
    
    @staticmethod
    def get_trade_by_ticket(db: Session, account_id: UUID, ticket_id: str) -> Optional[Trade]:
        return db.query(Trade).filter(
            Trade.account_id == account_id,
            Trade.ticket_id == ticket_id
        ).first()
    
    @staticmethod
    def get_trades_by_account(db: Session, account_id: UUID, 
                            skip: int = 0, limit: int = 100) -> List[Trade]:
        return db.query(Trade).filter(
            Trade.account_id == account_id
        ).order_by(Trade.open_time.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_open_trades_by_account(db: Session, account_id: UUID) -> List[Trade]:
        return db.query(Trade).filter(
            Trade.account_id == account_id,
            Trade.status == "open"
        ).all()
    
    @staticmethod
    def create_trade(db: Session, trade_data: dict) -> Trade:
        # Check for duplicate ticket_id
        existing_trade = TradeRepository.get_trade_by_ticket(
            db, trade_data['account_id'], trade_data['ticket_id']
        )
        if existing_trade:
            raise ValueError(f"Trade with ticket_id {trade_data['ticket_id']} already exists for this account")
        
        db_trade = Trade(**trade_data)
        db.add(db_trade)
        db.commit()
        db.refresh(db_trade)
        return db_trade
    
    @staticmethod
    def update_trade(db: Session, trade_id: UUID, trade_data: dict) -> Trade:
        trade = TradeRepository.get_trade_by_id(db, trade_id)
        if trade:
            for key, value in trade_data.items():
                if value is not None:
                    setattr(trade, key, value)
            db.commit()
            db.refresh(trade)
        return trade
    
    @staticmethod
    def get_account_trading_summary(db: Session, account_id: UUID) -> dict:
        """Get trading summary statistics for an account"""
        # Get total trades count
        total_trades = db.query(Trade).filter(
            Trade.account_id == account_id
        ).count()
        
        # Get winning/losing trades
        winning_trades = db.query(Trade).filter(
            Trade.account_id == account_id,
            Trade.profit > 0
        ).count()
        
        losing_trades = db.query(Trade).filter(
            Trade.account_id == account_id,
            Trade.profit < 0
        ).count()
        
        # Get total profit/loss
        total_profit = db.query(Trade.profit).filter(
            Trade.account_id == account_id
        ).scalar() or Decimal('0')
        
        # Get total commission and swap
        total_commission = db.query(Trade.commission).filter(
            Trade.account_id == account_id
        ).scalar() or Decimal('0')
        
        total_swap = db.query(Trade.swap).filter(
            Trade.account_id == account_id
        ).scalar() or Decimal('0')
        
        # Get account info
        account = db.query(Account).filter(Account.id == account_id).first()
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": (Decimal(winning_trades) / Decimal(total_trades) * 100) if total_trades > 0 else Decimal('0'),
            "total_profit": total_profit,
            "total_commission": total_commission,
            "total_swap": total_swap,
            "current_balance": account.current_balance if account else Decimal('0'),
            "current_equity": account.equity if account else Decimal('0'),
            "highest_balance": account.highest_balance if account else Decimal('0'),
            "last_trade_time": db.query(Trade.close_time).filter(
                Trade.account_id == account_id,
                Trade.close_time.isnot(None)
            ).order_by(Trade.close_time.desc()).first()
        }

class DailyStatRepository:
    """Repository for daily statistics operations"""
    
    @staticmethod
    def get_daily_stat_by_id(db: Session, stat_id: UUID) -> Optional[DailyStat]:
        return db.query(DailyStat).filter(DailyStat.id == stat_id).first()
    
    @staticmethod
    def get_daily_stat_by_date(db: Session, account_id: UUID, stat_date: date) -> Optional[DailyStat]:
        # Convert date to datetime with UTC timezone
        stat_datetime = datetime.combine(stat_date, datetime.min.time().replace(tzinfo=pytz.UTC))
        return db.query(DailyStat).filter(
            DailyStat.account_id == account_id,
            DailyStat.stat_date == stat_datetime
        ).first()
    
    @staticmethod
    def get_daily_stats_by_account(db: Session, account_id: UUID, 
                                 days: int = 30) -> List[DailyStat]:
        from datetime import timedelta
        cutoff_date = datetime.now(pytz.UTC) - timedelta(days=days)
        return db.query(DailyStat).filter(
            DailyStat.account_id == account_id,
            DailyStat.stat_date >= cutoff_date
        ).order_by(DailyStat.stat_date.desc()).all()
    
    @staticmethod
    def create_daily_stat(db: Session, stat_data: dict) -> DailyStat:
        # Check if stat already exists for this date
        existing_stat = DailyStatRepository.get_daily_stat_by_date(
            db, stat_data['account_id'], stat_data['stat_date'].date()
        )
        if existing_stat:
            # Update existing stat instead of creating new one
            return DailyStatRepository.update_daily_stat(db, existing_stat.id, stat_data)
        
        db_stat = DailyStat(**stat_data)
        db.add(db_stat)
        db.commit()
        db.refresh(db_stat)
        return db_stat
    
    @staticmethod
    def update_daily_stat(db: Session, stat_id: UUID, stat_data: dict) -> DailyStat:
        stat = DailyStatRepository.get_daily_stat_by_id(db, stat_id)
        if stat:
            for key, value in stat_data.items():
                if value is not None:
                    setattr(stat, key, value)
            db.commit()
            db.refresh(stat)
        return stat
    
    @staticmethod
    def calculate_daily_stats(db: Session, account_id: UUID, stat_date: date) -> dict:
        """Calculate daily statistics for an account"""
        from datetime import datetime, timedelta
        
        # Convert date to datetime range
        start_datetime = datetime.combine(stat_date, datetime.min.time().replace(tzinfo=pytz.UTC))
        end_datetime = start_datetime + timedelta(days=1)
        
        # Get trades for the day
        day_trades = db.query(Trade).filter(
            Trade.account_id == account_id,
            Trade.close_time >= start_datetime,
            Trade.close_time < end_datetime
        ).all()
        
        # Calculate statistics
        trade_count = len(day_trades)
        winning_trades = len([t for t in day_trades if t.profit > 0])
        losing_trades = len([t for t in day_trades if t.profit < 0])
        
        total_commission = sum(t.commission or Decimal('0') for t in day_trades)
        total_swap = sum(t.swap or Decimal('0') for t in day_trades)
        daily_pnl = sum(t.profit or Decimal('0') for t in day_trades)
        
        # Get account balance at start and end of day
        account = db.query(Account).filter(Account.id == account_id).first()
        starting_balance = account.daily_start_balance if account else Decimal('0')
        ending_balance = account.current_balance if account else Decimal('0')
        
        return {
            "account_id": account_id,
            "stat_date": start_datetime,
            "starting_balance": starting_balance,
            "ending_balance": ending_balance,
            "daily_pnl": daily_pnl,
            "total_commission": total_commission,
            "total_swap": total_swap,
            "trade_count": trade_count,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "max_drawdown": Decimal('0')  # This would need more complex calculation
        }

class EquitySnapshotRepository:
    """Repository for equity snapshot operations"""
    
    @staticmethod
    def create_snapshot(db: Session, snapshot_data: dict) -> EquitySnapshot:
        db_snapshot = EquitySnapshot(**snapshot_data)
        db.add(db_snapshot)
        db.commit()
        db.refresh(db_snapshot)
        return db_snapshot
    
    @staticmethod
    def get_latest_snapshot(db: Session, account_id: UUID) -> Optional[EquitySnapshot]:
        return db.query(EquitySnapshot).filter(
            EquitySnapshot.account_id == account_id
        ).order_by(EquitySnapshot.timestamp.desc()).first()
    
    @staticmethod
    def get_snapshots_by_account(db: Session, account_id: UUID, 
                               hours: int = 24) -> List[EquitySnapshot]:
        from datetime import timedelta
        cutoff_time = datetime.now(pytz.UTC) - timedelta(hours=hours)
        return db.query(EquitySnapshot).filter(
            EquitySnapshot.account_id == account_id,
            EquitySnapshot.timestamp >= cutoff_time
        ).order_by(EquitySnapshot.timestamp.desc()).all()

class MT5SyncLogRepository:
    """Repository for MT5 sync log operations"""
    
    @staticmethod
    def create_sync_log(db: Session, log_data: dict) -> MT5SyncLog:
        db_log = MT5SyncLog(**log_data)
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def get_sync_logs_by_account(db: Session, account_id: UUID, 
                               limit: int = 100) -> List[MT5SyncLog]:
        return db.query(MT5SyncLog).filter(
            MT5SyncLog.account_id == account_id
        ).order_by(MT5SyncLog.sync_started_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_recent_sync_status(db: Session, account_id: UUID) -> Optional[MT5SyncLog]:
        return db.query(MT5SyncLog).filter(
            MT5SyncLog.account_id == account_id
        ).order_by(MT5SyncLog.sync_started_at.desc()).first()