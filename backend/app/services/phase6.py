from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional, Tuple
from app.models.phase6.mt5 import MT5Server, MT5Account, MT5Trade, MT5ServerStatusEnum, MT5AccountStatusEnum, MT5TradeStatusEnum
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase3.trading import Trade
from app.schemas.phase6 import (
    MT5AccountCreate, MT5AccountUpdate, MT5TradeCreate, MT5TradeUpdate,
    MT5ConnectionStatus, MT5SyncResponse, MT5BalanceUpdate
)
from app.core.config import settings
from app.core.logger import get_logger
import pytz
import time
import uuid

logger = get_logger(__name__)

class MT5Service:
    """Service for MT5 integration and trade synchronization"""
    
    @staticmethod
    def get_connection_status(db: Session) -> List[MT5ConnectionStatus]:
        """Get connection status for all MT5 servers"""
        try:
            servers = db.query(MT5Server).filter(
                MT5Server.status == MT5ServerStatusEnum.ACTIVE
            ).all()
            
            status_list = []
            for server in servers:
                # Get connected accounts count
                connected_accounts = db.query(func.count(MT5Account.id)).filter(
                    MT5Account.server_id == server.id,
                    MT5Account.status == MT5AccountStatusEnum.CONNECTED
                ).scalar()
                
                # Get next scheduled sync
                next_sync = db.query(func.min(MT5Account.next_sync_time)).filter(
                    MT5Account.server_id == server.id,
                    MT5Account.status == MT5AccountStatusEnum.CONNECTED
                ).scalar()
                
                status = MT5ConnectionStatus(
                    server_id=server.id,
                    server_name=server.name,
                    status=server.status.value,
                    connected_accounts=connected_accounts,
                    last_heartbeat=server.last_heartbeat,
                    next_scheduled_sync=next_sync
                )
                status_list.append(status)
            
            return status_list
            
        except Exception as e:
            logger.error(f"Error getting MT5 connection status: {str(e)}")
            raise

    @staticmethod
    def create_mt5_account(db: Session, account_data: MT5AccountCreate) -> MT5Account:
        """Create a new MT5 account link"""
        try:
            # Verify user exists
            user = db.query(User).filter(User.id == account_data.user_id).first()
            if not user:
                raise ValueError(f"User {account_data.user_id} not found")
            
            # Verify server exists and is active
            server = db.query(MT5Server).filter(
                MT5Server.id == account_data.server_id,
                MT5Server.status == MT5ServerStatusEnum.ACTIVE
            ).first()
            if not server:
                raise ValueError(f"Active server {account_data.server_id} not found")
            
            # Verify platform account exists
            platform_account = db.query(Account).filter(
                Account.id == account_data.platform_account_id,
                Account.user_id == account_data.user_id
            ).first()
            if not platform_account:
                raise ValueError(f"Platform account {account_data.platform_account_id} not found for user")
            
            # Check if MT5 login already exists
            existing_account = db.query(MT5Account).filter(
                MT5Account.mt5_login == account_data.mt5_login
            ).first()
            if existing_account:
                raise ValueError(f"MT5 account {account_data.mt5_login} already exists")
            
            # Create MT5 account
            mt5_account = MT5Account(
                user_id=account_data.user_id,
                server_id=account_data.server_id,
                platform_account_id=account_data.platform_account_id,
                mt5_login=account_data.mt5_login,
                mt5_password=account_data.mt5_password,
                mt5_investor_password=account_data.mt5_investor_password,
                currency=account_data.currency,
                leverage=account_data.leverage,
                is_demo=account_data.is_demo,
                sync_interval_seconds=account_data.sync_interval_seconds,
                status=MT5AccountStatusEnum.DISCONNECTED
            )
            
            db.add(mt5_account)
            db.commit()
            db.refresh(mt5_account)
            
            logger.info(f"MT5 account created for user {user.username}: {mt5_account.mt5_login}")
            return mt5_account
            
        except Exception as e:
            logger.error(f"Error creating MT5 account: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def connect_mt5_account(db: Session, account_id: str, user_id: str = None) -> MT5Account:
        """Connect to an MT5 account"""
        try:
            # Get MT5 account
            query = db.query(MT5Account).filter(MT5Account.id == account_id)
            if user_id:
                query = query.filter(MT5Account.user_id == user_id)
            
            mt5_account = query.first()
            if not mt5_account:
                raise ValueError(f"MT5 account {account_id} not found")
            
            # Verify server is active
            server = db.query(MT5Server).filter(
                MT5Server.id == mt5_account.server_id,
                MT5Server.status == MT5ServerStatusEnum.ACTIVE
            ).first()
            if not server:
                raise ValueError("MT5 server is not active")
            
            # Simulate connection (in real implementation, this would connect to actual MT5)
            try:
                # This is where you'd implement actual MT5 connection logic
                # For now, we'll simulate a successful connection
                connection_success = True
                error_message = None
                
                if connection_success:
                    mt5_account.status = MT5AccountStatusEnum.CONNECTED
                    mt5_account.error_count = 0
                    mt5_account.last_error = None
                    mt5_account.last_error_time = None
                    
                    # Set next sync time
                    mt5_account.next_sync_time = datetime.utcnow() + timedelta(
                        seconds=mt5_account.sync_interval_seconds
                    )
                    
                    # Update server connection count
                    server.current_connections += 1
                    server.last_heartbeat = datetime.utcnow()
                    
                    logger.info(f"MT5 account connected: {mt5_account.mt5_login}")
                else:
                    mt5_account.status = MT5AccountStatusEnum.ERROR
                    mt5_account.error_count += 1
                    mt5_account.last_error = error_message
                    mt5_account.last_error_time = datetime.utcnow()
                    
                    logger.error(f"MT5 connection failed for {mt5_account.mt5_login}: {error_message}")
                
                db.commit()
                db.refresh(mt5_account)
                return mt5_account
                
            except Exception as e:
                # Handle connection errors
                mt5_account.status = MT5AccountStatusEnum.ERROR
                mt5_account.error_count += 1
                mt5_account.last_error = str(e)
                mt5_account.last_error_time = datetime.utcnow()
                
                db.commit()
                raise ValueError(f"Connection failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error connecting MT5 account: {str(e)}")
            raise

    @staticmethod
    def sync_mt5_trades(db: Session, account_id: str = None, server_id: str = None) -> MT5SyncResponse:
        """Synchronize trades from MT5 to platform"""
        try:
            start_time = time.time()
            
            # Get accounts to sync
            query = db.query(MT5Account).filter(
                MT5Account.status == MT5AccountStatusEnum.CONNECTED
            )
            
            if account_id:
                query = query.filter(MT5Account.id == account_id)
            elif server_id:
                query = query.filter(MT5Account.server_id == server_id)
            
            accounts = query.all()
            
            if not accounts:
                return MT5SyncResponse(
                    success=True,
                    accounts_processed=0,
                    trades_imported=0,
                    sync_duration_ms=0
                )
            
            accounts_processed = 0
            trades_imported = 0
            
            for account in accounts:
                try:
                    # Update account status to syncing
                    account.status = MT5AccountStatusEnum.SYNCING
                    account.last_sync_time = datetime.utcnow()
                    db.commit()
                    
                    # Simulate MT5 trade retrieval (in real implementation, call MT5 API)
                    mt5_trades = MT5Service._get_mt5_trades_from_api(account)
                    
                    # Process each trade
                    for mt5_trade_data in mt5_trades:
                        try:
                            # Check if trade already exists
                            existing_trade = db.query(MT5Trade).filter(
                                MT5Trade.account_id == account.id,
                                MT5Trade.mt5_ticket == mt5_trade_data['mt5_ticket']
                            ).first()
                            
                            if existing_trade:
                                # Update existing trade
                                MT5Service._update_existing_trade(db, existing_trade, mt5_trade_data)
                            else:
                                # Create new trade
                                MT5Service._create_new_trade(db, account, mt5_trade_data)
                                trades_imported += 1
                    
                        except Exception as e:
                            logger.error(f"Error processing trade {mt5_trade_data.get('mt5_ticket')}: {str(e)}")
                            continue
                    
                    # Update account balance information
                    MT5Service._update_account_balance(db, account)
                    
                    # Update account status
                    account.status = MT5AccountStatusEnum.CONNECTED
                    account.next_sync_time = datetime.utcnow() + timedelta(
                        seconds=account.sync_interval_seconds
                    )
                    accounts_processed += 1
                    
                except Exception as e:
                    logger.error(f"Error syncing account {account.mt5_login}: {str(e)}")
                    account.status = MT5AccountStatusEnum.ERROR
                    account.error_count += 1
                    account.last_error = str(e)
                    account.last_error_time = datetime.utcnow()
                    continue
            
            db.commit()
            
            sync_duration = int((time.time() - start_time) * 1000)
            
            return MT5SyncResponse(
                success=True,
                accounts_processed=accounts_processed,
                trades_imported=trades_imported,
                sync_duration_ms=sync_duration,
                next_sync_scheduled=datetime.utcnow() + timedelta(minutes=1)
            )
            
        except Exception as e:
            logger.error(f"Error synchronizing MT5 trades: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def _get_mt5_trades_from_api(account: MT5Account) -> List[Dict]:
        """Simulate getting trades from MT5 API (replace with actual MT5 integration)"""
        # This is a placeholder - in real implementation, you'd call MT5 Manager API
        # or use a MT5 bridge/connector to get actual trade data
        
        # Simulate some trades for demonstration
        simulated_trades = [
            {
                'mt5_ticket': f"{account.mt5_login}_1001",
                'symbol': 'EURUSD',
                'direction': 'buy',
                'volume': Decimal('0.1'),
                'price_open': Decimal('1.12345'),
                'time_open': datetime.utcnow() - timedelta(hours=2),
                'status': 'open'
            },
            {
                'mt5_ticket': f"{account.mt5_login}_1002",
                'symbol': 'GBPUSD',
                'direction': 'sell',
                'volume': Decimal('0.05'),
                'price_open': Decimal('1.23456'),
                'price_close': Decimal('1.23410'),
                'time_open': datetime.utcnow() - timedelta(hours=1),
                'time_close': datetime.utcnow() - timedelta(minutes=30),
                'profit': Decimal('-2.30'),
                'status': 'closed'
            }
        ]
        
        return simulated_trades

    @staticmethod
    def _create_new_trade(db: Session, account: MT5Account, trade_data: Dict) -> MT5Trade:
        """Create a new trade from MT5 data"""
        try:
            # Create MT5 trade record
            mt5_trade = MT5Trade(
                account_id=account.id,
                mt5_ticket=trade_data['mt5_ticket'],
                symbol=trade_data['symbol'],
                direction=trade_data['direction'],
                volume=trade_data['volume'],
                price_open=trade_data['price_open'],
                time_open=trade_data['time_open'],
                status=trade_data.get('status', 'open')
            )
            
            # Add optional fields
            if 'price_close' in trade_data:
                mt5_trade.price_close = trade_data['price_close']
            if 'time_close' in trade_data:
                mt5_trade.time_close = trade_data['time_close']
            if 'profit' in trade_data:
                mt5_trade.profit = trade_data['profit']
            if 'swap' in trade_data:
                mt5_trade.swap = trade_data['swap']
            if 'commission' in trade_data:
                mt5_trade.commission = trade_data['commission']
            if 'sl' in trade_data:
                mt5_trade.sl = trade_data['sl']
            if 'tp' in trade_data:
                mt5_trade.tp = trade_data['tp']
            if 'comment' in trade_data:
                mt5_trade.comment = trade_data['comment']
            
            db.add(mt5_trade)
            db.flush()  # Get the ID without committing
            
            # Create corresponding platform trade if it doesn't exist
            if not db.query(Trade).filter(Trade.id == mt5_trade.id).first():
                platform_trade = Trade(
                    account_id=account.platform_account_id,
                    ticket_id=mt5_trade.mt5_ticket,
                    symbol=mt5_trade.symbol,
                    order_type=mt5_trade.direction.upper(),
                    volume=mt5_trade.volume,
                    open_price=mt5_trade.price_open,
                    open_time=mt5_trade.time_open,
                    profit=mt5_trade.profit or Decimal('0'),
                    commission=mt5_trade.commission or Decimal('0'),
                    swap=mt5_trade.swap or Decimal('0'),
                    comment=mt5_trade.comment
                )
                
                if mt5_trade.price_close:
                    platform_trade.close_price = mt5_trade.price_close
                if mt5_trade.time_close:
                    platform_trade.close_time = mt5_trade.time_close
                
                db.add(platform_trade)
                db.flush()
                
                # Link the trades
                mt5_trade.platform_trade_id = platform_trade.id
            
            db.commit()
            return mt5_trade
            
        except Exception as e:
            logger.error(f"Error creating new trade: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def _update_existing_trade(db: Session, mt5_trade: MT5Trade, trade_data: Dict) -> MT5Trade:
        """Update an existing trade with new MT5 data"""
        try:
            # Update trade fields that may have changed
            if 'price_close' in trade_data:
                mt5_trade.price_close = trade_data['price_close']
            if 'time_close' in trade_data:
                mt5_trade.time_close = trade_data['time_close']
            if 'time_update' in trade_data:
                mt5_trade.time_update = trade_data['time_update']
            if 'status' in trade_data:
                mt5_trade.status = trade_data['status']
            if 'profit' in trade_data:
                mt5_trade.profit = trade_data['profit']
            if 'swap' in trade_data:
                mt5_trade.swap = trade_data['swap']
            if 'commission' in trade_data:
                mt5_trade.commission = trade_data['commission']
            if 'reason' in trade_data:
                mt5_trade.reason = trade_data['reason']
            
            # Update linked platform trade if it exists
            if mt5_trade.platform_trade_id:
                platform_trade = db.query(Trade).filter(
                    Trade.id == mt5_trade.platform_trade_id
                ).first()
                
                if platform_trade:
                    if 'price_close' in trade_data:
                        platform_trade.close_price = trade_data['price_close']
                    if 'time_close' in trade_data:
                        platform_trade.close_time = trade_data['time_close']
                    if 'profit' in trade_data:
                        platform_trade.profit = trade_data['profit']
                    if 'swap' in trade_data:
                        platform_trade.swap = trade_data['swap']
                    if 'commission' in trade_data:
                        platform_trade.commission = trade_data['commission']
            
            db.commit()
            db.refresh(mt5_trade)
            return mt5_trade
            
        except Exception as e:
            logger.error(f"Error updating trade {mt5_trade.mt5_ticket}: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def _update_account_balance(db: Session, account: MT5Account) -> None:
        """Update account balance information from MT5"""
        try:
            # Simulate getting balance from MT5 (replace with actual API call)
            # In real implementation, you'd call MT5 API to get current balance/equity
            
            # For demonstration, we'll simulate some balance changes
            account.balance = Decimal('10000.00')
            account.equity = Decimal('10050.00')
            account.margin = Decimal('1000.00')
            account.free_margin = Decimal('9050.00')
            account.margin_level = Decimal('1005.00')
            
            # Update platform account balance
            platform_account = db.query(Account).filter(
                Account.id == account.platform_account_id
            ).first()
            
            if platform_account:
                platform_account.current_balance = account.equity
                if account.equity > (platform_account.max_balance or 0):
                    platform_account.max_balance = account.equity
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error updating account balance for {account.mt5_login}: {str(e)}")
            db.rollback()

    @staticmethod
    def get_mt5_account(db: Session, account_id: str, user_id: str = None) -> MT5Account:
        """Get MT5 account details"""
        try:
            query = db.query(MT5Account).filter(MT5Account.id == account_id)
            if user_id:
                query = query.filter(MT5Account.user_id == user_id)
            
            account = query.first()
            if not account:
                raise ValueError(f"MT5 account {account_id} not found")
            
            return account
            
        except Exception as e:
            logger.error(f"Error getting MT5 account: {str(e)}")
            raise

    @staticmethod
    def get_user_mt5_accounts(db: Session, user_id: str) -> List[MT5Account]:
        """Get all MT5 accounts for a user"""
        try:
            accounts = db.query(MT5Account).filter(
                MT5Account.user_id == user_id
            ).all()
            return accounts
            
        except Exception as e:
            logger.error(f"Error getting user MT5 accounts: {str(e)}")
            raise

    @staticmethod
    def disconnect_mt5_account(db: Session, account_id: str, user_id: str = None) -> MT5Account:
        """Disconnect from an MT5 account"""
        try:
            query = db.query(MT5Account).filter(MT5Account.id == account_id)
            if user_id:
                query = query.filter(MT5Account.user_id == user_id)
            
            account = query.first()
            if not account:
                raise ValueError(f"MT5 account {account_id} not found")
            
            # Update status
            account.status = MT5AccountStatusEnum.DISCONNECTED
            account.next_sync_time = None
            
            # Update server connection count
            server = db.query(MT5Server).filter(MT5Server.id == account.server_id).first()
            if server and server.current_connections > 0:
                server.current_connections -= 1
            
            db.commit()
            db.refresh(account)
            
            logger.info(f"MT5 account disconnected: {account.mt5_login}")
            return account
            
        except Exception as e:
            logger.error(f"Error disconnecting MT5 account: {str(e)}")
            db.rollback()
            raise