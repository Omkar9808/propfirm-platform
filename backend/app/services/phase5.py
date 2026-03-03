from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional, Tuple
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase3.trading import Trade
from app.models.phase3.trading import DailyStat as DailyStats
from app.models.phase5.analytics import TraderMetrics, PlatformMetrics, LeaderboardCache
from app.schemas.phase5 import (
    TraderMetricsCreate, TraderMetricsUpdate, PlatformMetricsCreate,
    TraderPerformanceSummary, PlatformOverview
)
from app.core.config import settings
from app.core.logger import get_logger
import math

logger = get_logger(__name__)

class AnalyticsService:
    """Service for calculating and aggregating analytics data"""
    
    @staticmethod
    def calculate_trader_metrics(db: Session, user_id: str) -> TraderMetrics:
        """Calculate comprehensive metrics for a single trader"""
        try:
            # Get user and accounts
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            accounts = db.query(Account).filter(Account.user_id == user_id).all()
            
            # Initialize metrics
            metrics = {
                'total_accounts': len(accounts),
                'active_accounts': len([a for a in accounts if a.status == 'active']),
                'passed_accounts': len([a for a in accounts if a.status == 'passed']),
                'failed_accounts': len([a for a in accounts if a.status == 'failed']),
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_profit': Decimal('0'),
                'total_loss': Decimal('0'),
                'total_commission': Decimal('0'),
                'total_swap': Decimal('0'),
                'max_drawdown': Decimal('0'),
                'avg_daily_loss': Decimal('0'),
                'max_consecutive_losses': 0,
                'days_traded': 0,
                'avg_trades_per_day': Decimal('0'),
                'last_trade_date': None,
                'win_rate': Decimal('0'),
                'profit_factor': Decimal('0'),
                'sharpe_ratio': Decimal('0'),
                'risk_reward_ratio': Decimal('0'),
                'is_active_trader': False,
                'ranking_score': Decimal('0')
            }
            
            # Calculate trading metrics
            if accounts:
                account_ids = [a.id for a in accounts]
                
                # Get trades
                trades = db.query(Trade).filter(Trade.account_id.in_(account_ids)).all()
                metrics['total_trades'] = len(trades)
                
                # Calculate profit/loss metrics
                for trade in trades:
                    profit = trade.profit or Decimal('0')
                    commission = trade.commission or Decimal('0')
                    swap = trade.swap or Decimal('0')
                    
                    metrics['total_commission'] += commission
                    metrics['total_swap'] += swap
                    
                    if profit > 0:
                        metrics['winning_trades'] += 1
                        metrics['total_profit'] += profit
                    else:
                        metrics['losing_trades'] += 1
                        metrics['total_loss'] += abs(profit)
                
                # Calculate daily stats for risk metrics
                daily_stats = db.query(DailyStats).filter(
                    DailyStats.account_id.in_(account_ids)
                ).all()
                
                if daily_stats:
                    daily_losses = [stat.daily_loss for stat in daily_stats if stat.daily_loss < 0]
                    if daily_losses:
                        metrics['avg_daily_loss'] = Decimal(str(sum(daily_losses) / len(daily_losses)))
                        metrics['max_drawdown'] = min(daily_losses)  # Most negative drawdown
                    
                    # Calculate max consecutive losses
                    consecutive_losses = 0
                    max_consecutive = 0
                    for stat in daily_stats:
                        if stat.daily_loss < 0:
                            consecutive_losses += 1
                            max_consecutive = max(max_consecutive, consecutive_losses)
                        else:
                            consecutive_losses = 0
                    metrics['max_consecutive_losses'] = max_consecutive
                    
                    # Trading days and frequency
                    unique_dates = set(stat.stat_date.date() for stat in daily_stats)
                    metrics['days_traded'] = len(unique_dates)
                    
                    if metrics['days_traded'] > 0:
                        metrics['avg_trades_per_day'] = Decimal(str(metrics['total_trades'] / metrics['days_traded']))
                    
                    # Last trade date
                    last_trade = db.query(Trade).filter(
                        Trade.account_id.in_(account_ids)
                    ).order_by(Trade.close_time.desc()).first()
                    if last_trade:
                        metrics['last_trade_date'] = last_trade.close_time
                
                # Calculate derived metrics
                if metrics['total_trades'] > 0:
                    metrics['win_rate'] = Decimal(str((metrics['winning_trades'] / metrics['total_trades']) * 100))
                    metrics['is_active_trader'] = metrics['days_traded'] > 30  # Active if traded > 30 days
                
                # Profit factor (gross profit / gross loss)
                if metrics['total_loss'] > 0:
                    metrics['profit_factor'] = metrics['total_profit'] / metrics['total_loss']
                
                # Risk-reward ratio (simplified)
                if metrics['losing_trades'] > 0:
                    avg_win = metrics['total_profit'] / metrics['winning_trades'] if metrics['winning_trades'] > 0 else Decimal('0')
                    avg_loss = metrics['total_loss'] / metrics['losing_trades']
                    if avg_loss > 0:
                        metrics['risk_reward_ratio'] = avg_win / avg_loss
                
                # Sharpe ratio (simplified)
                if daily_stats:
                    returns = [stat.daily_pnl for stat in daily_stats]
                    if len(returns) > 1:
                        avg_return = sum(returns) / len(returns)
                        std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
                        if std_dev > 0:
                            metrics['sharpe_ratio'] = avg_return / std_dev
                
                # Calculate ranking score (weighted combination of key metrics)
                ranking_components = [
                    (metrics['win_rate'] / 100) * 0.3,  # 30% weight
                    (min(metrics['profit_factor'], Decimal('5')) / 5) * 0.25,  # 25% weight (capped)
                    (max(100 - metrics['max_consecutive_losses'], 0) / 100) * 0.2,  # 20% weight
                    (min(metrics['sharpe_ratio'], Decimal('3')) / 3) * 0.15,  # 15% weight (capped)
                    (min(metrics['days_traded'] / 365, 1)) * 0.1  # 10% weight
                ]
                metrics['ranking_score'] = Decimal(str(sum(ranking_components) * 100))
            
            # Create or update trader metrics
            existing_metrics = db.query(TraderMetrics).filter(
                TraderMetrics.user_id == user_id
            ).first()
            
            if existing_metrics:
                for key, value in metrics.items():
                    setattr(existing_metrics, key, value)
                db.commit()
                db.refresh(existing_metrics)
                return existing_metrics
            else:
                trader_metrics = TraderMetrics(**metrics, user_id=user_id)
                db.add(trader_metrics)
                db.commit()
                db.refresh(trader_metrics)
                return trader_metrics
                
        except Exception as e:
            logger.error(f"Error calculating trader metrics for user {user_id}: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def calculate_all_trader_metrics(db: Session) -> dict:
        """Calculate metrics for all traders"""
        try:
            users = db.query(User).all()
            processed_count = 0
            
            for user in users:
                try:
                    AnalyticsService.calculate_trader_metrics(db, user.id)
                    processed_count += 1
                except Exception as e:
                    logger.error(f"Failed to calculate metrics for user {user.id}: {str(e)}")
                    continue
            
            return {
                "success": True,
                "processed_traders": processed_count,
                "total_traders": len(users)
            }
            
        except Exception as e:
            logger.error(f"Error calculating all trader metrics: {str(e)}")
            raise

    @staticmethod
    def generate_platform_metrics(db: Session, target_date: datetime = None) -> PlatformMetrics:
        """Generate daily platform metrics snapshot"""
        try:
            if not target_date:
                target_date = datetime.utcnow().date()
            
            # Convert to datetime if it's a date
            if hasattr(target_date, 'date'):
                target_date = datetime.combine(target_date.date(), datetime.min.time())
            
            # Check if metrics already exist for this date
            existing_metrics = db.query(PlatformMetrics).filter(
                func.date(PlatformMetrics.metric_date) == target_date.date()
            ).first()
            
            if existing_metrics:
                return existing_metrics
            
            # Calculate user metrics
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            new_users = db.query(User).filter(
                func.date(User.created_at) == target_date.date()
            ).count()
            
            # Calculate account metrics
            total_accounts = db.query(Account).count()
            active_accounts = db.query(Account).filter(Account.status == 'active').count()
            passed_accounts = db.query(Account).filter(Account.status == 'passed').count()
            failed_accounts = db.query(Account).filter(Account.status == 'failed').count()
            new_accounts = db.query(Account).filter(
                func.date(Account.created_at) == target_date.date()
            ).count()
            
            # Calculate trading metrics
            total_trades = db.query(Trade).filter(
                func.date(Trade.close_time) == target_date.date()
            ).count()
            
            # Calculate volume and revenue
            daily_trades = db.query(Trade).filter(
                func.date(Trade.close_time) == target_date.date()
            ).all()
            
            total_volume = sum(abs(trade.volume) for trade in daily_trades) if daily_trades else Decimal('0')
            
            # Calculate platform equity (simplified)
            accounts_with_balance = db.query(Account).filter(
                Account.status.in_(['active', 'passed'])
            ).all()
            total_platform_equity = sum(
                acc.current_balance for acc in accounts_with_balance if acc.current_balance
            ) or Decimal('0')
            
            avg_account_balance = (
                total_platform_equity / len(accounts_with_balance)
                if accounts_with_balance else Decimal('0')
            )
            
            # Calculate win rate
            if daily_trades:
                winning_trades = sum(1 for trade in daily_trades if (trade.profit or 0) > 0)
                avg_win_rate = Decimal(str((winning_trades / len(daily_trades)) * 100))
            else:
                avg_win_rate = Decimal('0')
            
            # Calculate payout ratio
            payout_ratio = (
                Decimal(str((passed_accounts / total_accounts) * 100))
                if total_accounts > 0 else Decimal('0')
            )
            
            # System metrics (simplified)
            sync_success_rate = Decimal('100')  # Would come from sync logs
            risk_evaluation_success_rate = Decimal('100')  # Would come from job logs
            
            # Create platform metrics
            platform_metrics = PlatformMetrics(
                metric_date=target_date,
                total_users=total_users,
                active_users=active_users,
                new_users=new_users,
                total_accounts=total_accounts,
                active_accounts=active_accounts,
                passed_accounts=passed_accounts,
                failed_accounts=failed_accounts,
                new_accounts=new_accounts,
                total_trades=total_trades,
                total_volume=total_volume,
                total_revenue=Decimal('0'),  # Would be calculated from payments
                avg_account_balance=avg_account_balance,
                total_platform_equity=total_platform_equity,
                payout_ratio=payout_ratio,
                avg_win_rate=avg_win_rate,
                platform_drawdown=Decimal('0'),  # Would calculate from equity history
                sync_success_rate=sync_success_rate,
                risk_evaluation_success_rate=risk_evaluation_success_rate
            )
            
            db.add(platform_metrics)
            db.commit()
            db.refresh(platform_metrics)
            
            return platform_metrics
            
        except Exception as e:
            logger.error(f"Error generating platform metrics: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def get_platform_overview(db: Session) -> PlatformOverview:
        """Get current platform overview statistics"""
        try:
            # Get current counts
            total_users = db.query(User).count()
            total_accounts = db.query(Account).count()
            active_accounts = db.query(Account).filter(Account.status == 'active').count()
            passed_accounts = db.query(Account).filter(Account.status == 'passed').count()
            failed_accounts = db.query(Account).filter(Account.status == 'failed').count()
            total_trades = db.query(Trade).count()
            
            # Calculate aggregates
            total_revenue = Decimal('0')  # Would come from payment/revenue data
            avg_win_rate = Decimal('0')
            payout_ratio = (
                Decimal(str((passed_accounts / total_accounts) * 100))
                if total_accounts > 0 else Decimal('0')
            )
            
            # Calculate average win rate from trader metrics
            trader_metrics = db.query(TraderMetrics).filter(
                TraderMetrics.win_rate > 0
            ).all()
            
            if trader_metrics:
                avg_win_rate = sum(tm.win_rate for tm in trader_metrics) / len(trader_metrics)
            
            return PlatformOverview(
                total_users=total_users,
                total_accounts=total_accounts,
                active_accounts=active_accounts,
                passed_accounts=passed_accounts,
                failed_accounts=failed_accounts,
                total_trades=total_trades,
                total_revenue=total_revenue,
                avg_win_rate=avg_win_rate,
                payout_ratio=payout_ratio,
                last_updated=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error getting platform overview: {str(e)}")
            raise

    @staticmethod
    def get_trader_performance_summary(db: Session, user_id: str) -> TraderPerformanceSummary:
        """Get comprehensive performance summary for a trader"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Get trader metrics
            trader_metrics = db.query(TraderMetrics).filter(
                TraderMetrics.user_id == user_id
            ).first()
            
            if not trader_metrics:
                trader_metrics = AnalyticsService.calculate_trader_metrics(db, user_id)
            
            # Get account summary
            accounts = db.query(Account).filter(Account.user_id == user_id).all()
            account_summary = {
                'total': len(accounts),
                'by_status': {
                    'active': len([a for a in accounts if a.status == 'active']),
                    'passed': len([a for a in accounts if a.status == 'passed']),
                    'failed': len([a for a in accounts if a.status == 'failed'])
                },
                'total_balance': sum(a.current_balance or 0 for a in accounts)
            }
            
            # Get recent activity
            recent_trades = db.query(Trade).join(Account).filter(
                Account.user_id == user_id
            ).order_by(Trade.close_time.desc()).limit(5).all()
            
            recent_activity = {
                'recent_trades': [
                    {
                        'symbol': trade.symbol,
                        'profit': float(trade.profit or 0),
                        'close_time': trade.close_time
                    } for trade in recent_trades
                ]
            }
            
            return TraderPerformanceSummary(
                user_id=user.id,
                username=user.username,
                email=user.email,
                trader_metrics=trader_metrics,
                account_summary=account_summary,
                recent_activity=recent_activity
            )
            
        except Exception as e:
            logger.error(f"Error getting trader performance summary: {str(e)}")
            raise