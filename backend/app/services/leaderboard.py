from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, delete
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional
from app.models.user import User
from app.models.phase5.analytics import TraderMetrics, LeaderboardCache, LeaderboardPeriodEnum
from app.schemas.phase5 import LeaderboardEntry, LeaderboardCacheCreate
from app.core.logger import get_logger

logger = get_logger(__name__)

class LeaderboardService:
    """Service for generating and managing leaderboard rankings"""
    
    @staticmethod
    def generate_leaderboard(db: Session, period: str = "all_time", limit: int = 100) -> List[LeaderboardEntry]:
        """Generate leaderboard for a specific period"""
        try:
            # Validate period
            valid_periods = ["daily", "weekly", "monthly", "all_time"]
            if period not in valid_periods:
                raise ValueError(f"Invalid period: {period}. Must be one of {valid_periods}")
            
            # Calculate date range for the period
            period_start, period_end = LeaderboardService._get_period_dates(period)
            
            # Query trader metrics with ranking
            query = db.query(
                TraderMetrics,
                User.username,
                func.rank().over(
                    order_by=desc(TraderMetrics.ranking_score),
                    partition_by=None
                ).label('rank')
            ).join(User).filter(
                TraderMetrics.is_active_trader == True,
                TraderMetrics.ranking_score > 0
            )
            
            # Apply period filter if not all_time
            if period != "all_time":
                # For period-specific rankings, we'd need to filter based on recent activity
                # This is a simplified approach - in production, you'd have historical metrics
                query = query.filter(
                    TraderMetrics.last_trade_date >= period_start
                )
            
            # Order by ranking score and limit results
            ranked_traders = query.order_by(desc(TraderMetrics.ranking_score)).limit(limit).all()
            
            # Convert to leaderboard entries
            leaderboard = []
            for trader_metrics, username, rank in ranked_traders:
                entry = LeaderboardEntry(
                    rank=int(rank),
                    user_id=trader_metrics.user_id,
                    username=username,
                    win_rate=trader_metrics.win_rate,
                    total_profit=trader_metrics.total_profit,
                    trades_count=trader_metrics.total_trades,
                    ranking_score=trader_metrics.ranking_score,
                    period=period
                )
                leaderboard.append(entry)
            
            return leaderboard
            
        except Exception as e:
            logger.error(f"Error generating leaderboard for period {period}: {str(e)}")
            raise

    @staticmethod
    def update_leaderboard_cache(db: Session) -> dict:
        """Update cached leaderboard entries for all periods"""
        try:
            # Clear existing cache
            db.execute(delete(LeaderboardCache))
            db.commit()
            
            periods = ["daily", "weekly", "monthly", "all_time"]
            cache_entries = []
            total_entries = 0
            
            for period in periods:
                try:
                    # Generate leaderboard for this period
                    leaderboard = LeaderboardService.generate_leaderboard(db, period, limit=1000)
                    
                    # Get period dates
                    period_start, period_end = LeaderboardService._get_period_dates(period)
                    
                    # Create cache entries
                    for entry in leaderboard:
                        cache_entry = LeaderboardCache(
                            period=period,
                            rank=entry.rank,
                            user_id=entry.user_id,
                            win_rate=entry.win_rate,
                            total_profit=entry.total_profit,
                            trades_count=entry.trades_count,
                            ranking_score=entry.ranking_score,
                            period_start=period_start,
                            period_end=period_end
                        )
                        cache_entries.append(cache_entry)
                        total_entries += 1
                    
                except Exception as e:
                    logger.error(f"Error updating leaderboard cache for period {period}: {str(e)}")
                    continue
            
            # Bulk insert cache entries
            if cache_entries:
                db.bulk_save_objects(cache_entries)
                db.commit()
            
            return {
                "success": True,
                "updated_periods": periods,
                "total_entries": total_entries,
                "updated_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error updating leaderboard cache: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def get_cached_leaderboard(db: Session, period: str = "all_time", limit: int = 100) -> List[LeaderboardEntry]:
        """Get cached leaderboard data for a specific period"""
        try:
            # Validate period
            if period not in ["daily", "weekly", "monthly", "all_time"]:
                raise ValueError(f"Invalid period: {period}")
            
            # Query cached leaderboard entries
            cache_entries = db.query(LeaderboardCache).join(User).filter(
                LeaderboardCache.period == period
            ).order_by(LeaderboardCache.rank).limit(limit).all()
            
            # Convert to leaderboard entries
            leaderboard = []
            for entry in cache_entries:
                leaderboard_entry = LeaderboardEntry(
                    rank=int(entry.rank),
                    user_id=entry.user_id,
                    username=entry.user.username,  # From relationship
                    win_rate=entry.win_rate,
                    total_profit=entry.total_profit,
                    trades_count=entry.trades_count,
                    ranking_score=entry.ranking_score,
                    period=period
                )
                leaderboard.append(leaderboard_entry)
            
            return leaderboard
            
        except Exception as e:
            logger.error(f"Error getting cached leaderboard for period {period}: {str(e)}")
            raise

    @staticmethod
    def get_user_ranking(db: Session, user_id: str, period: str = "all_time") -> Optional[LeaderboardEntry]:
        """Get a specific user's ranking for a period"""
        try:
            # Check cached data first
            cache_entry = db.query(LeaderboardCache).join(User).filter(
                LeaderboardCache.user_id == user_id,
                LeaderboardCache.period == period
            ).first()
            
            if cache_entry:
                return LeaderboardEntry(
                    rank=int(cache_entry.rank),
                    user_id=cache_entry.user_id,
                    username=cache_entry.user.username,
                    win_rate=cache_entry.win_rate,
                    total_profit=cache_entry.total_profit,
                    trades_count=cache_entry.trades_count,
                    ranking_score=cache_entry.ranking_score,
                    period=period
                )
            
            # If not in cache, calculate live ranking
            leaderboard = LeaderboardService.generate_leaderboard(db, period, limit=1000)
            
            for entry in leaderboard:
                if str(entry.user_id) == str(user_id):
                    return entry
            
            return None  # User not ranked
            
        except Exception as e:
            logger.error(f"Error getting user ranking: {str(e)}")
            raise

    @staticmethod
    def get_leaderboard_statistics(db: Session) -> dict:
        """Get statistics about leaderboard data"""
        try:
            stats = {}
            
            # Get entry counts by period
            period_stats = db.query(
                LeaderboardCache.period,
                func.count(LeaderboardCache.id).label('entry_count'),
                func.max(LeaderboardCache.ranking_score).label('max_score'),
                func.avg(LeaderboardCache.ranking_score).label('avg_score')
            ).group_by(LeaderboardCache.period).all()
            
            for period_stat in period_stats:
                stats[period_stat.period] = {
                    'entry_count': period_stat.entry_count,
                    'max_score': float(period_stat.max_score or 0),
                    'avg_score': float(period_stat.avg_score or 0)
                }
            
            # Get last update time
            last_update = db.query(func.max(LeaderboardCache.calculated_at)).scalar()
            
            # Get total unique traders
            unique_traders = db.query(func.count(func.distinct(LeaderboardCache.user_id))).scalar()
            
            return {
                'periods': stats,
                'total_unique_traders': unique_traders,
                'last_updated': last_update,
                'is_cache_current': last_update and (datetime.utcnow() - last_update).total_seconds() < 3600  # 1 hour
            }
            
        except Exception as e:
            logger.error(f"Error getting leaderboard statistics: {str(e)}")
            raise

    @staticmethod
    def _get_period_dates(period: str) -> tuple:
        """Get start and end dates for a given period"""
        now = datetime.utcnow()
        
        if period == "daily":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == "weekly":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(weeks=1)
        elif period == "monthly":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end = now.replace(year=now.year + 1, month=1, day=1)
            else:
                end = now.replace(month=now.month + 1, day=1)
        else:  # all_time
            start = datetime(2020, 1, 1)  # Platform start date
            end = now + timedelta(days=1)
        
        return start, end

    @staticmethod
    def should_update_leaderboard(db: Session) -> bool:
        """Check if leaderboard cache should be updated"""
        try:
            # Check when last updated
            last_update = db.query(func.max(LeaderboardCache.calculated_at)).scalar()
            
            if not last_update:
                return True  # Never updated
            
            # Update if more than 1 hour old
            time_since_update = datetime.utcnow() - last_update
            return time_since_update.total_seconds() > 3600
            
        except Exception as e:
            logger.error(f"Error checking leaderboard update status: {str(e)}")
            return True  # Default to update if check fails

    @staticmethod
    def get_top_traders_by_metric(db: Session, metric: str = "ranking_score", limit: int = 10) -> List[dict]:
        """Get top traders by specific metric"""
        try:
            valid_metrics = ["ranking_score", "win_rate", "total_profit", "total_trades"]
            if metric not in valid_metrics:
                raise ValueError(f"Invalid metric: {metric}")
            
            # Query top traders by metric
            query = db.query(
                TraderMetrics,
                User.username
            ).join(User).filter(
                getattr(TraderMetrics, metric) > 0
            ).order_by(desc(getattr(TraderMetrics, metric))).limit(limit)
            
            results = query.all()
            
            top_traders = []
            for trader_metrics, username in results:
                trader_data = {
                    'user_id': trader_metrics.user_id,
                    'username': username,
                    'metric_value': float(getattr(trader_metrics, metric)),
                    'total_trades': int(trader_metrics.total_trades),
                    'win_rate': float(trader_metrics.win_rate),
                    'total_profit': float(trader_metrics.total_profit)
                }
                top_traders.append(trader_data)
            
            return top_traders
            
        except Exception as e:
            logger.error(f"Error getting top traders by {metric}: {str(e)}")
            raise