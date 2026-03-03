from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.repositories.phase4 import (
    ViolationRepository, AccountStatusHistoryRepository, JobExecutionLogRepository
)
from app.repositories.phase3 import TradeRepository, DailyStatRepository
from app.repositories.phase2 import AccountRepository, AccountRuleSnapshotRepository
from app.models.user import User
from app.models.phase2.account import Account, AccountStatusEnum
from app.models.phase4.risk import ViolationTypeEnum
from app.schemas.phase4 import (
    RiskMetrics, RuleViolation, RiskEvaluationResult, 
    AccountRiskStatus, ManualAccountAction
)
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import pytz
import time

class RiskEngineService:
    """Core risk engine service for automated account evaluation"""
    
    @staticmethod
    def _get_account_with_lock(db: Session, account_id: UUID) -> Account:
        """Get account with SELECT FOR UPDATE locking for concurrency safety"""
        from sqlalchemy import text
        
        # Use raw SQL with SELECT FOR UPDATE for maximum concurrency safety
        result = db.execute(
            text("""
                SELECT * FROM accounts 
                WHERE id = :account_id 
                FOR UPDATE
            """),
            {"account_id": account_id}
        ).fetchone()
        
        if not result:
            return None
            
        # Convert result to Account object
        account = db.query(Account).filter(Account.id == account_id).first()
        return account
    
    @staticmethod
    def _was_recently_evaluated(account: Account, threshold_seconds: int = 60) -> bool:
        """Check if account was evaluated recently to prevent race conditions"""
        if not hasattr(account, 'last_evaluated_at') or not account.last_evaluated_at:
            return False
            
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        last_eval = account.last_evaluated_at.replace(tzinfo=timezone.utc)
        time_diff = (now - last_eval).total_seconds()
        
        return time_diff < threshold_seconds
    
    @staticmethod
    def evaluate_account_risk(db: Session, account_id: UUID) -> RiskEvaluationResult:
        """Evaluate a single account for risk violations with concurrency protection"""
        start_time = time.time()
        
        try:
            # Get account with concurrency locking
            account = RiskEngineService._get_account_with_lock(db, account_id)
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )
            
            # Check if recently evaluated (race condition protection)
            if RiskEngineService._was_recently_evaluated(account):
                return RiskEvaluationResult(
                    account_id=account.id,
                    account_number=account.account_number,
                    evaluation_time=datetime.now(pytz.UTC),
                    is_compliant=True,
                    violations=[],
                    risk_metrics=RiskEngineService._calculate_risk_metrics(db, account, account.rule_snapshot)
                )
            
            rule_snapshot = AccountRuleSnapshotRepository.get_snapshot_by_account(db, account_id)
            if not rule_snapshot:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Account rule snapshot not found"
                )
            
            # Calculate risk metrics
            risk_metrics = RiskEngineService._calculate_risk_metrics(db, account, rule_snapshot)
            
            # Check for violations with precedence logic
            violations = RiskEngineService._check_rule_violations(risk_metrics, rule_snapshot)
            
            # Determine compliance status
            is_compliant = len(violations) == 0
            
            # Prepare result
            result = RiskEvaluationResult(
                account_id=account.id,
                account_number=account.account_number,
                evaluation_time=datetime.now(pytz.UTC),
                is_compliant=is_compliant,
                violations=violations,
                risk_metrics=risk_metrics
            )
            
            # Handle status changes if violations found
            if not is_compliant:
                RiskEngineService._handle_violations(db, account, violations, result)
                
            # Update evaluation timestamp for race condition protection
            from datetime import datetime, timezone
            account.last_evaluated_at = datetime.now(timezone.utc)
            
            # All database operations in transaction
            db.commit()
            
            return result
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Risk evaluation failed: {str(e)}"
            )
    
    @staticmethod
    def evaluate_all_active_accounts(db: Session) -> dict:
        """Evaluate all active accounts and return summary"""
        start_time = time.time()
        
        # Get all active accounts
        active_accounts = db.query(Account).filter(
            Account.status == AccountStatusEnum.ACTIVE
        ).all()
        
        # Log job execution start
        job_log = JobExecutionLogRepository.create_job_log(db, {
            "job_name": "risk_evaluation_batch",
            "job_type": "risk_evaluation",
            "status": "in_progress",
            "started_at": datetime.now(pytz.UTC),
            "accounts_processed": len(active_accounts),
            "triggered_by": "system"
        })
        
        try:
            results = []
            accounts_passed = 0
            accounts_failed = 0
            total_violations = 0
            
            for account in active_accounts:
                try:
                    result = RiskEngineService.evaluate_account_risk(db, account.id)
                    results.append(result)
                    
                    if result.is_compliant:
                        accounts_passed += 1
                    else:
                        accounts_failed += 1
                        total_violations += len(result.violations)
                        
                except Exception as e:
                    print(f"Error evaluating account {account.account_number}: {e}")
                    continue
            
            # Update job log with completion
            completion_time = datetime.now(pytz.UTC)
            JobExecutionLogRepository.update_job_log(db, job_log.id, {
                "status": "success",
                "completed_at": completion_time,
                "duration_ms": int((time.time() - start_time) * 1000),
                "accounts_passed": accounts_passed,
                "accounts_failed": accounts_failed,
                "violations_created": total_violations
            })
            
            return {
                "job_id": job_log.id,
                "evaluated_accounts": len(active_accounts),
                "accounts_passed": accounts_passed,
                "accounts_failed": accounts_failed,
                "total_violations": total_violations,
                "duration_ms": int((time.time() - start_time) * 1000),
                "results": results
            }
            
        except Exception as e:
            # Log job failure
            JobExecutionLogRepository.update_job_log(db, job_log.id, {
                "status": "failed",
                "completed_at": datetime.now(pytz.UTC),
                "duration_ms": int((time.time() - start_time) * 1000),
                "error_message": str(e)
            })
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Risk evaluation failed: {str(e)}"
            )
    
    @staticmethod
    def get_account_risk_status(db: Session, user: User, account_id: UUID) -> AccountRiskStatus:
        """Get comprehensive risk status for an account"""
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
        
        # Get violation summary
        violation_summary = ViolationRepository.get_violation_summary(db, account_id)
        
        # Get current status
        current_status = AccountStatusHistoryRepository.get_account_current_status(db, account_id)
        
        # Calculate risk score (simplified)
        risk_score = RiskEngineService._calculate_risk_score(
            violation_summary["active_violations"],
            account.status
        )
        
        return AccountRiskStatus(
            account_id=account.id,
            account_number=account.account_number,
            current_status=current_status or account.status,
            active_violations=violation_summary["active_violations"],
            total_violations=violation_summary["total_violations"],
            days_active=account.passed_at.days if account.passed_at else 0,
            risk_score=risk_score
        )
    
    @staticmethod
    def manual_account_action(db: Session, user: User, action_data: ManualAccountAction) -> dict:
        """Admin override for account status"""
        if user.role.name not in ["super_admin", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform manual account actions"
            )
        
        account = AccountRepository.get_account_by_id(db, action_data.account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Validate action
        valid_actions = ["pass", "fail", "lock", "unlock"]
        if action_data.action not in valid_actions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid action. Must be one of: {valid_actions}"
            )
        
        # Map action to status
        status_mapping = {
            "pass": AccountStatusEnum.PASSED,
            "fail": AccountStatusEnum.FAILED,
            "lock": AccountStatusEnum.LOCKED,
            "unlock": AccountStatusEnum.ACTIVE
        }
        
        new_status = status_mapping[action_data.action]
        
        # Create violation for manual fail
        violation_id = None
        if action_data.action == "fail":
            violation = ViolationRepository.create_violation(db, {
                "account_id": account.id,
                "violation_type": ViolationTypeEnum.MANUAL_FAIL,
                "description": f"Manual fail by {user.username}: {action_data.reason}",
                "current_value": account.current_balance,
                "threshold_value": account.starting_balance
            })
            violation_id = violation.id
        
        # Update account status
        AccountRepository.update_account_status(
            db, account.id, new_status,
            locked_by=user.id if action_data.action == "lock" else None,
            locked_reason=action_data.reason if action_data.action == "lock" else None
        )
        
        # Create status history
        AccountStatusHistoryRepository.create_status_change(db, {
            "account_id": account.id,
            "from_status": account.status,
            "to_status": new_status,
            "changed_by": user.id,
            "change_reason": f"Manual {action_data.action} by {user.username}",
            "change_notes": action_data.notes,
            "violation_id": violation_id
        })
        
        return {
            "account_id": account.id,
            "previous_status": account.status,
            "new_status": new_status,
            "action_performed_by": user.username,
            "reason": action_data.reason
        }
    
    @staticmethod
    def _calculate_risk_metrics(db: Session, account: Account, rule_snapshot) -> RiskMetrics:
        """Calculate comprehensive risk metrics for an account with formalized drawdown logic"""
        # Basic balance calculations
        starting_balance = account.starting_balance
        current_balance = account.current_balance
        current_equity = account.equity if account.equity > 0 else current_balance
        highest_balance = account.highest_balance
        
        # Enhanced Daily Drawdown Calculation (UTC reset)
        daily_start_balance = RiskEngineService._get_daily_start_balance(account, db)
        daily_drawdown = daily_start_balance - current_equity if daily_start_balance else Decimal('0')
        daily_drawdown_percent = (daily_drawdown / starting_balance * 100) if starting_balance > 0 else Decimal('0')
        
        # Maximum Drawdown (Static Model - lifetime calculation)
        max_drawdown = starting_balance - highest_balance
        max_drawdown_percent = (max_drawdown / starting_balance * 100) if starting_balance > 0 else Decimal('0')
        
        # Trailing Drawdown (if enabled in rule snapshot)
        trailing_drawdown = Decimal('0')
        trailing_drawdown_percent = Decimal('0')
        trailing_enabled = getattr(rule_snapshot, 'drawdown_mode', 'DAILY') == 'TRAILING'
        
        if trailing_enabled and hasattr(rule_snapshot, 'max_drawdown_percent'):
            drawdown_limit = (highest_balance * rule_snapshot.max_drawdown_percent / 100)
            trailing_drawdown = max(highest_balance - current_equity - drawdown_limit, Decimal('0'))
            trailing_drawdown_percent = (trailing_drawdown / highest_balance * 100) if highest_balance > 0 else Decimal('0')
        
        # Total Loss Calculation
        total_loss = starting_balance - current_equity
        total_loss_percent = (total_loss / starting_balance * 100) if starting_balance > 0 else Decimal('0')
        
        # Profit calculations (using equity for accuracy)
        profit = current_equity - starting_balance
        profit_percent = (profit / starting_balance * 100) if starting_balance > 0 else Decimal('0')
        profit_target = rule_snapshot.profit_target
        profit_target_percent = (profit_target / starting_balance * 100) if starting_balance > 0 else Decimal('0')
        
        # Trade metrics with enhanced data
        trading_summary = TradeRepository.get_account_trading_summary(db, account.id)
        
        # Enhanced risk metrics with proper drawdown tracking
        return RiskMetrics(
            account_id=account.id,
            account_number=account.account_number,
            current_balance=current_balance,
            current_equity=current_equity,
            starting_balance=starting_balance,
            highest_balance=highest_balance,
            daily_start_balance=daily_start_balance,
            daily_drawdown=daily_drawdown,
            daily_drawdown_percent=daily_drawdown_percent,
            max_drawdown=max_drawdown,
            max_drawdown_percent=max_drawdown_percent,
            trailing_drawdown=trailing_drawdown,
            trailing_drawdown_percent=trailing_drawdown_percent,
            trailing_enabled=trailing_enabled,
            total_loss=total_loss,
            total_loss_percent=total_loss_percent,
            profit=profit,
            profit_percent=profit_percent,
            profit_target=profit_target,
            profit_target_percent=profit_target_percent,
            open_positions=trading_summary.get("total_trades", 0),
            max_positions_allowed=rule_snapshot.max_positions,
            largest_position=Decimal('0'),  # Position sizing calculation needed
            total_trades=trading_summary.get("total_trades", 0),
            winning_trades=trading_summary.get("winning_trades", 0),
            losing_trades=trading_summary.get("losing_trades", 0),
            win_rate=trading_summary.get("win_rate", Decimal('0'))
        )
    
    @staticmethod
    def _check_rule_violations(risk_metrics: RiskMetrics, rule_snapshot) -> List[RuleViolation]:
        """Check for rule violations with formalized precedence hierarchy"""
        violations = []
        
        # Priority 1: Hard Violations (Immediate Fail)
        hard_violations = []
        
        # 1. Max Total Loss Exceeded
        if risk_metrics.total_loss > rule_snapshot.max_total_loss:
            hard_violations.append(RuleViolation(
                violation_type=ViolationTypeEnum.TOTAL_LOSS_EXCEEDED,
                description=f"Total loss {risk_metrics.total_loss} exceeds limit {rule_snapshot.max_total_loss}",
                current_value=risk_metrics.total_loss,
                threshold_value=rule_snapshot.max_total_loss,
                is_breached=True
            ))
        
        # 2. Trailing Drawdown Breach (if enabled)
        if risk_metrics.trailing_enabled and risk_metrics.trailing_drawdown > 0:
            hard_violations.append(RuleViolation(
                violation_type="TRAILING_DRAW_DOWN_BREACH",
                description=f"Trailing drawdown {risk_metrics.trailing_drawdown} breached limit",
                current_value=risk_metrics.trailing_drawdown,
                threshold_value=Decimal('0'),
                is_breached=True
            ))
        
        # 3. Max Lot Size Breach (would need trade-level checking)
        # This would be implemented in trade processing service
        
        # Priority 2: Daily Violations
        daily_violations = []
        
        # Daily Loss Exceeded
        if risk_metrics.daily_drawdown > rule_snapshot.max_daily_loss:
            daily_violations.append(RuleViolation(
                violation_type=ViolationTypeEnum.DAILY_LOSS_EXCEEDED,
                description=f"Daily drawdown {risk_metrics.daily_drawdown} exceeds limit {rule_snapshot.max_daily_loss}",
                current_value=risk_metrics.daily_drawdown,
                threshold_value=rule_snapshot.max_daily_loss,
                is_breached=True
            ))
        
        # Position Limit Exceeded
        if risk_metrics.open_positions > rule_snapshot.max_positions:
            daily_violations.append(RuleViolation(
                violation_type=ViolationTypeEnum.MAX_POSITIONS_EXCEEDED,
                description=f"Open positions {risk_metrics.open_positions} exceeds limit {rule_snapshot.max_positions}",
                current_value=Decimal(risk_metrics.open_positions),
                threshold_value=Decimal(rule_snapshot.max_positions),
                is_breached=True
            ))
        
        # Priority 3: Soft Warnings (would be implemented separately)
        
        # Priority 4: Success Conditions (Only if no hard violations)
        success_conditions = []
        
        if not hard_violations and risk_metrics.profit >= rule_snapshot.profit_target:
            success_conditions.append(RuleViolation(
                violation_type="PROFIT_TARGET_ACHIEVED",
                description=f"Profit target {risk_metrics.profit} achieved (target: {rule_snapshot.profit_target})",
                current_value=risk_metrics.profit,
                threshold_value=rule_snapshot.profit_target,
                is_breached=True
            ))
        
        # Apply precedence: Hard violations take priority
        if hard_violations:
            violations.extend(hard_violations)
        elif daily_violations:
            violations.extend(daily_violations)
        elif success_conditions:
            violations.extend(success_conditions)
        
        return violations
    
    @staticmethod
    def _prevent_duplicate_violations(db: Session, account_id: UUID, violation_type: str, evaluation_window_hours: int = 24) -> bool:
        """Check if a violation of this type was already recorded recently to prevent duplicates"""
        from datetime import datetime, timedelta, timezone
        from app.models.phase4.risk import Violation
        
        window_start = datetime.now(timezone.utc) - timedelta(hours=evaluation_window_hours)
        
        existing_violation = db.query(Violation).filter(
            Violation.account_id == account_id,
            Violation.violation_type == violation_type,
            Violation.created_at >= window_start,
            Violation.is_resolved == False
        ).first()
        
        return existing_violation is not None
    
    @staticmethod
    def _handle_violations(db: Session, account: Account, violations: List[RuleViolation], 
                          evaluation_result: RiskEvaluationResult) -> None:
        """Handle violations by creating records and updating account status with safeguards"""
        # Create violation records with duplicate prevention
        violations_to_create = []
        for violation in violations:
            # Check for recent duplicate violations
            if not RiskEngineService._prevent_duplicate_violations(
                db, account.id, violation.violation_type
            ):
                violations_to_create.append(violation)
        
        # Create only non-duplicate violation records
        for violation in violations_to_create:
            ViolationRepository.create_violation(db, {
                "account_id": account.id,
                "violation_type": violation.violation_type,
                "description": violation.description,
                "current_value": violation.current_value,
                "threshold_value": violation.threshold_value
            })
        
        # If critical violations, fail the account
        critical_violations = [
            ViolationTypeEnum.TOTAL_LOSS_EXCEEDED,
            "TRAILING_DRAW_DOWN_BREACH"
        ]
        
        has_critical_violation = any(
            v.violation_type in critical_violations for v in violations
        )
        
        # Prevent double status change
        if has_critical_violation and account.status != AccountStatusEnum.FAILED:
            # Update account status to failed
            AccountRepository.update_account_status(
                db, account.id, AccountStatusEnum.FAILED
            )
            
            # Create status history atomically
            AccountStatusHistoryRepository.create_status_change(db, {
                "account_id": account.id,
                "from_status": account.status,
                "to_status": AccountStatusEnum.FAILED,
                "changed_by": None,  # System change
                "change_reason": "Risk rule violation",
                "change_notes": f"Failed due to violations: {[v.violation_type for v in violations_to_create]}"
            })
            
            evaluation_result.status_change = "failed"
            evaluation_result.status_reason = "Account failed due to risk violations"
        
        # Handle success conditions (profit target achieved)
        success_violations = [v for v in violations if v.violation_type == "PROFIT_TARGET_ACHIEVED"]
        if success_violations and account.status != AccountStatusEnum.PASSED:
            # Update account status to passed
            AccountRepository.update_account_status(
                db, account.id, AccountStatusEnum.PASSED
            )
            
            # Create status history
            AccountStatusHistoryRepository.create_status_change(db, {
                "account_id": account.id,
                "from_status": account.status,
                "to_status": AccountStatusEnum.PASSED,
                "changed_by": None,  # System change
                "change_reason": "Profit target achieved",
                "change_notes": f"Passed with profit: {success_violations[0].current_value}"
            })
            
            evaluation_result.status_change = "passed"
            evaluation_result.status_reason = "Account passed with profit target achievement"
    
    @staticmethod
    def _get_daily_start_balance(account: Account, db: Session) -> Decimal:
        """Get daily start balance with UTC midnight reset logic"""
        from datetime import datetime, timezone
        from app.repositories.phase3 import EquitySnapshotRepository
        
        now_utc = datetime.now(timezone.utc)
        today_midnight = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check if we have a daily_start_balance set and it's from today
        if account.daily_start_balance and account.updated_at:
            # If last updated was today, use existing daily_start_balance
            if account.updated_at.replace(tzinfo=timezone.utc) >= today_midnight:
                return account.daily_start_balance
        
        # Get equity snapshot from exactly at today's midnight UTC
        midnight_equity = EquitySnapshotRepository.get_equity_at_time(
            db, account.id, today_midnight
        )
        
        if midnight_equity:
            return midnight_equity.equity
        
        # Fallback: use current equity if no midnight snapshot
        return account.equity if account.equity > 0 else account.current_balance
    
    @staticmethod
    def _calculate_risk_score(active_violations: int, account_status: str) -> Decimal:
        """Calculate risk score (0-100, where 0 is lowest risk)"""
        # Base score based on violations
        base_score = min(active_violations * 25, 75)  # 25 points per violation, max 75
        
        # Status modifiers
        status_modifiers = {
            "failed": 25,
            "locked": 20,
            "active": 0,
            "passed": -20
        }
        
        modifier = status_modifiers.get(account_status, 0)
        final_score = min(max(base_score + modifier, 0), 100)
        
        return Decimal(str(final_score))