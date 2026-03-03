from sqlalchemy.orm import Session
from app.models.phase5.analytics import TraderMetrics
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase3.trading import Trade, DailyStat
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import statistics

class EnhancedTraderMetricsService:
    @staticmethod
    def calculate_scaling_indicators(db: Session, user_id: uuid.UUID) -> Dict:
        """Calculate advanced scaling indicators for a trader"""
        # Get trader metrics
        trader_metrics = db.query(TraderMetrics).filter(
            TraderMetrics.user_id == user_id
        ).first()
        
        if not trader_metrics:
            return {}
        
        # Calculate tier level based on performance
        tier_level = EnhancedTraderMetricsService._calculate_tier_level(trader_metrics)
        
        # Calculate tier progress (0-100%)
        tier_progress = EnhancedTraderMetricsService._calculate_tier_progress(trader_metrics, tier_level)
        
        # Calculate scaling multiplier
        scaling_multiplier = EnhancedTraderMetricsService._calculate_scaling_multiplier(tier_level, tier_progress)
        
        # Calculate consistency score
        consistency_score = EnhancedTraderMetricsService._calculate_consistency_score(db, user_id)
        
        # Calculate momentum indicators
        momentum_data = EnhancedTraderMetricsService._calculate_momentum_indicators(db, user_id)
        
        # Calculate advanced risk metrics
        risk_metrics = EnhancedTraderMetricsService._calculate_advanced_risk_metrics(db, user_id)
        
        return {
            "tier_level": int(tier_level),
            "tier_progress": float(tier_progress),
            "scaling_multiplier": float(scaling_multiplier),
            "consistency_score": float(consistency_score),
            "performance_momentum": float(momentum_data["momentum"]),
            "streak_length": int(momentum_data["streak_length"]),
            "streak_type": momentum_data["streak_type"],
            "value_at_risk": float(risk_metrics["var"]),
            "expected_shortfall": float(risk_metrics["es"]),
            "tail_risk": float(risk_metrics["tail_risk"])
        }

    @staticmethod
    def _calculate_tier_level(metrics: TraderMetrics) -> int:
        """Calculate current tier level based on performance metrics"""
        # Tier 1: Basic requirements
        if metrics.passed_accounts >= 1 and metrics.win_rate >= 50:
            # Tier 2: Intermediate requirements
            if metrics.passed_accounts >= 3 and metrics.win_rate >= 55 and metrics.profit_factor >= 1.2:
                # Tier 3: Advanced requirements
                if metrics.passed_accounts >= 5 and metrics.win_rate >= 60 and metrics.profit_factor >= 1.5:
                    # Tier 4: Elite requirements
                    if metrics.passed_accounts >= 10 and metrics.win_rate >= 65 and metrics.profit_factor >= 2.0:
                        return 4
                    return 3
                return 2
            return 1
        return 1

    @staticmethod
    def _calculate_tier_progress(metrics: TraderMetrics, current_tier: int) -> Decimal:
        """Calculate progress percentage to next tier"""
        tier_requirements = {
            1: {"passed_accounts": 1, "win_rate": 50, "profit_factor": 1.0},
            2: {"passed_accounts": 3, "win_rate": 55, "profit_factor": 1.2},
            3: {"passed_accounts": 5, "win_rate": 60, "profit_factor": 1.5},
            4: {"passed_accounts": 10, "win_rate": 65, "profit_factor": 2.0}
        }
        
        if current_tier >= 4:
            return Decimal('100.00')
        
        next_tier = current_tier + 1
        req = tier_requirements[next_tier]
        
        # Calculate progress based on key metrics
        progress_metrics = []
        
        # Passed accounts progress
        accounts_progress = min(Decimal('100.00'), 
            (Decimal(str(metrics.passed_accounts)) / Decimal(str(req["passed_accounts"]))) * Decimal('25.00'))
        progress_metrics.append(accounts_progress)
        
        # Win rate progress
        win_rate_progress = min(Decimal('100.00'), 
            (Decimal(str(metrics.win_rate)) / Decimal(str(req["win_rate"]))) * Decimal('25.00'))
        progress_metrics.append(win_rate_progress)
        
        # Profit factor progress
        profit_factor_progress = min(Decimal('100.00'), 
            (Decimal(str(metrics.profit_factor)) / Decimal(str(req["profit_factor"]))) * Decimal('25.00'))
        progress_metrics.append(profit_factor_progress)
        
        # Activity progress (based on active accounts)
        activity_progress = min(Decimal('100.00'), 
            (Decimal(str(metrics.active_accounts)) / Decimal('1.0')) * Decimal('25.00'))
        progress_metrics.append(activity_progress)
        
        return sum(progress_metrics) / len(progress_metrics)

    @staticmethod
    def _calculate_scaling_multiplier(tier_level: int, tier_progress: Decimal) -> Decimal:
        """Calculate scaling multiplier based on tier and progress"""
        base_multipliers = {1: Decimal('1.0'), 2: Decimal('1.5'), 3: Decimal('2.0'), 4: Decimal('3.0')}
        base_multiplier = base_multipliers.get(tier_level, Decimal('1.0'))
        
        # Add progress-based bonus (up to 20% additional)
        progress_bonus = (tier_progress / Decimal('100.00')) * Decimal('0.20')
        
        return base_multiplier + progress_bonus

    @staticmethod
    def _calculate_consistency_score(db: Session, user_id: uuid.UUID) -> Decimal:
        """Calculate daily performance consistency score"""
        # Get daily stats for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        daily_stats = db.query(DailyStats).join(Account).filter(
            Account.user_id == user_id,
            DailyStats.date >= thirty_days_ago
        ).all()
        
        if not daily_stats:
            return Decimal('0.00')
        
        # Calculate daily returns
        daily_returns = []
        for stat in daily_stats:
            if stat.starting_balance > 0:
                daily_return = ((stat.ending_balance - stat.starting_balance) / stat.starting_balance) * 100
                daily_returns.append(float(daily_return))
        
        if len(daily_returns) < 5:  # Need minimum data
            return Decimal('0.00')
        
        # Calculate consistency using coefficient of variation
        mean_return = statistics.mean(daily_returns)
        if mean_return == 0:
            return Decimal('0.00')
            
        std_dev = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0
        cv = abs(std_dev / mean_return) if mean_return != 0 else 0
        
        # Convert to consistency score (lower CV = higher consistency)
        consistency_score = max(0, 100 - (cv * 10))  # Scale to 0-100
        return Decimal(str(min(100, consistency_score)))

    @staticmethod
    def _calculate_momentum_indicators(db: Session, user_id: uuid.UUID) -> Dict:
        """Calculate performance momentum and streak indicators"""
        # Get recent trades (last 50 trades)
        recent_trades = db.query(Trade).join(Account).filter(
            Account.user_id == user_id
        ).order_by(Trade.timestamp.desc()).limit(50).all()
        
        if not recent_trades:
            return {"momentum": 0, "streak_length": 0, "streak_type": None}
        
        # Calculate profit/loss for each trade
        trade_results = []
        for trade in recent_trades:
            result = trade.profit_loss
            trade_results.append(result)
        
        # Calculate momentum (recent vs older performance)
        if len(trade_results) >= 20:
            recent_avg = statistics.mean(trade_results[:10])
            older_avg = statistics.mean(trade_results[10:20])
            momentum = ((recent_avg - older_avg) / abs(older_avg) * 100) if older_avg != 0 else 0
        else:
            momentum = 0
        
        # Calculate streak
        streak_length = 0
        streak_type = None
        
        if trade_results:
            current_streak = 1
            current_type = "winning" if trade_results[0] > 0 else "losing"
            
            for i in range(1, len(trade_results)):
                trade_type = "winning" if trade_results[i] > 0 else "losing"
                if trade_type == current_type:
                    current_streak += 1
                else:
                    break
            
            streak_length = current_streak
            streak_type = current_type
        
        return {
            "momentum": momentum,
            "streak_length": streak_length,
            "streak_type": streak_type
        }

    @staticmethod
    def _calculate_advanced_risk_metrics(db: Session, user_id: uuid.UUID) -> Dict:
        """Calculate advanced risk metrics including VaR and tail risk"""
        # Get recent daily stats for risk calculation
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        daily_stats = db.query(DailyStats).join(Account).filter(
            Account.user_id == user_id,
            DailyStats.date >= ninety_days_ago
        ).all()
        
        if not daily_stats:
            return {"var": 0, "es": 0, "tail_risk": 0}
        
        # Calculate daily returns
        daily_returns = []
        for stat in daily_stats:
            if stat.starting_balance > 0:
                daily_return = (stat.ending_balance - stat.starting_balance) / stat.starting_balance
                daily_returns.append(float(daily_return))
        
        if len(daily_returns) < 30:
            return {"var": 0, "es": 0, "tail_risk": 0}
        
        # Sort returns for percentile calculations
        sorted_returns = sorted(daily_returns)
        
        # Calculate Value at Risk (95% confidence)
        var_index = int(len(sorted_returns) * 0.05)  # 5th percentile
        var_95 = sorted_returns[var_index] if var_index < len(sorted_returns) else sorted_returns[0]
        
        # Calculate Expected Shortfall (average of worst 5% returns)
        es_count = max(1, int(len(sorted_returns) * 0.05))
        es_returns = sorted_returns[:es_count]
        expected_shortfall = statistics.mean(es_returns) if es_returns else 0
        
        # Calculate tail risk (kurtosis of returns)
        if len(daily_returns) > 3:
            mean_return = statistics.mean(daily_returns)
            std_dev = statistics.stdev(daily_returns)
            if std_dev > 0:
                # Simplified kurtosis calculation
                kurtosis = sum(((r - mean_return) / std_dev) ** 4 for r in daily_returns) / len(daily_returns) - 3
                tail_risk = max(0, min(100, kurtosis * 10))  # Scale to 0-100
            else:
                tail_risk = 0
        else:
            tail_risk = 0
        
        return {
            "var": var_95,
            "es": expected_shortfall,
            "tail_risk": tail_risk
        }

    @staticmethod
    def update_trader_metrics_with_scaling(db: Session, user_id: uuid.UUID) -> Optional[TraderMetrics]:
        """Update trader metrics with advanced scaling indicators"""
        trader_metrics = db.query(TraderMetrics).filter(
            TraderMetrics.user_id == user_id
        ).first()
        
        if not trader_metrics:
            return None
        
        # Calculate new scaling indicators
        scaling_data = EnhancedTraderMetricsService.calculate_scaling_indicators(db, user_id)
        
        if scaling_data:
            # Update metrics
            trader_metrics.tier_level = scaling_data["tier_level"]
            trader_metrics.tier_progress = scaling_data["tier_progress"]
            trader_metrics.scaling_multiplier = scaling_data["scaling_multiplier"]
            trader_metrics.consistency_score = scaling_data["consistency_score"]
            trader_metrics.performance_momentum = scaling_data["performance_momentum"]
            trader_metrics.streak_length = scaling_data["streak_length"]
            trader_metrics.streak_type = scaling_data["streak_type"]
            trader_metrics.value_at_risk = scaling_data["value_at_risk"]
            trader_metrics.expected_shortfall = scaling_data["expected_shortfall"]
            trader_metrics.tail_risk = scaling_data["tail_risk"]
            
            # Update max tier reached
            trader_metrics.max_tier_reached = max(
                int(trader_metrics.max_tier_reached), 
                scaling_data["tier_level"]
            )
            
            db.commit()
            db.refresh(trader_metrics)
        
        return trader_metrics

    @staticmethod
    def get_trader_scaling_profile(db: Session, user_id: uuid.UUID) -> Dict:
        """Get complete trader scaling profile"""
        trader_metrics = db.query(TraderMetrics).filter(
            TraderMetrics.user_id == user_id
        ).first()
        
        if not trader_metrics:
            return {}
        
        scaling_data = EnhancedTraderMetricsService.calculate_scaling_indicators(db, user_id)
        
        return {
            "current_tier": int(trader_metrics.tier_level),
            "max_tier_reached": int(trader_metrics.max_tier_reached),
            "tier_progress": float(trader_metrics.tier_progress),
            "scaling_multiplier": float(trader_metrics.scaling_multiplier),
            "consistency_score": float(trader_metrics.consistency_score),
            "performance_momentum": float(trader_metrics.performance_momentum),
            "streak_info": {
                "length": int(trader_metrics.streak_length),
                "type": trader_metrics.streak_type
            },
            "risk_metrics": {
                "value_at_risk": float(trader_metrics.value_at_risk),
                "expected_shortfall": float(trader_metrics.expected_shortfall),
                "tail_risk": float(trader_metrics.tail_risk)
            },
            "performance_metrics": {
                "win_rate": float(trader_metrics.win_rate),
                "profit_factor": float(trader_metrics.profit_factor),
                "total_profit": float(trader_metrics.total_profit),
                "passed_accounts": int(trader_metrics.passed_accounts)
            }
        }