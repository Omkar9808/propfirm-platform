from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Optional
from app.models.user import User
from app.models.phase2.account import Account
from app.models.phase2.payment import Payment
from app.models.phase3.trading import Trade
from app.models.phase4.risk import Violation, AccountStatusHistory
from app.models.phase5.analytics import PlatformMetrics
from app.schemas.phase5 import (
    AdminDashboardMetrics, UserManagementAction, AccountManagementAction,
    RevenueReportRequest, RevenueReportResponse
)
from app.core.logger import get_logger
from app.core.security import get_password_hash
import uuid

logger = get_logger(__name__)

class AdminService:
    """Service for admin dashboard and management controls"""
    
    @staticmethod
    def get_dashboard_metrics(db: Session) -> AdminDashboardMetrics:
        """Get comprehensive dashboard metrics for admin panel"""
        try:
            # User metrics
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            suspended_users = db.query(User).filter(User.is_suspended == True).count()
            new_users_today = db.query(User).filter(
                func.date(User.created_at) == datetime.utcnow().date()
            ).count()
            
            user_metrics = {
                "total_users": total_users,
                "active_users": active_users,
                "suspended_users": suspended_users,
                "new_users_today": new_users_today,
                "active_percentage": (active_users / total_users * 100) if total_users > 0 else 0
            }
            
            # Account metrics
            total_accounts = db.query(Account).count()
            active_accounts = db.query(Account).filter(Account.status == 'active').count()
            passed_accounts = db.query(Account).filter(Account.status == 'passed').count()
            failed_accounts = db.query(Account).filter(Account.status == 'failed').count()
            pending_accounts = db.query(Account).filter(Account.status == 'pending').count()
            new_accounts_today = db.query(Account).filter(
                func.date(Account.created_at) == datetime.utcnow().date()
            ).count()
            
            account_metrics = {
                "total_accounts": total_accounts,
                "active_accounts": active_accounts,
                "passed_accounts": passed_accounts,
                "failed_accounts": failed_accounts,
                "pending_accounts": pending_accounts,
                "new_accounts_today": new_accounts_today,
                "pass_rate": (passed_accounts / total_accounts * 100) if total_accounts > 0 else 0
            }
            
            # Trading metrics
            total_trades = db.query(Trade).count()
            trades_today = db.query(Trade).filter(
                func.date(Trade.close_time) == datetime.utcnow().date()
            ).count()
            total_volume = db.query(func.sum(Trade.volume)).scalar() or Decimal('0')
            total_commission = db.query(func.sum(Trade.commission)).scalar() or Decimal('0')
            
            # Calculate today's trading volume
            today_volume = db.query(func.sum(Trade.volume)).filter(
                func.date(Trade.close_time) == datetime.utcnow().date()
            ).scalar() or Decimal('0')
            
            trading_metrics = {
                "total_trades": total_trades,
                "trades_today": trades_today,
                "total_volume": float(total_volume),
                "today_volume": float(today_volume),
                "total_commission": float(total_commission)
            }
            
            # Financial metrics
            total_payments = db.query(func.sum(Payment.amount)).filter(
                Payment.status == 'completed'
            ).scalar() or Decimal('0')
            
            total_revenue = db.query(func.sum(Payment.amount)).filter(
                Payment.status == 'completed',
                Payment.payment_type == 'challenge_purchase'
            ).scalar() or Decimal('0')
            
            pending_payments = db.query(Payment).filter(
                Payment.status == 'pending'
            ).count()
            
            financial_metrics = {
                "total_payments": float(total_payments),
                "total_revenue": float(total_revenue),
                "pending_payments": pending_payments,
                "average_payment": float(total_payments / total_users) if total_users > 0 else 0
            }
            
            # System metrics
            total_violations = db.query(Violation).count()
            active_violations = db.query(Violation).filter(
                Violation.is_active == True
            ).count()
            
            recent_violations = db.query(Violation).filter(
                Violation.created_at >= datetime.utcnow() - timedelta(days=7)
            ).count()
            
            system_metrics = {
                "total_violations": total_violations,
                "active_violations": active_violations,
                "recent_violations": recent_violations,
                "system_uptime": "100%"  # Would come from monitoring system
            }
            
            # Recent activity
            recent_activity = []
            
            # Recent user registrations
            recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
            for user in recent_users:
                recent_activity.append({
                    "type": "user_registration",
                    "user_id": user.id,
                    "username": user.username,
                    "timestamp": user.created_at,
                    "details": f"User {user.username} registered"
                })
            
            # Recent payments
            recent_payments = db.query(Payment).order_by(Payment.created_at.desc()).limit(5).all()
            for payment in recent_payments:
                recent_activity.append({
                    "type": "payment",
                    "user_id": payment.user_id,
                    "username": payment.user.username,
                    "timestamp": payment.created_at,
                    "details": f"Payment of ${payment.amount} for {payment.payment_type}"
                })
            
            # Recent account passes
            recent_passes = db.query(Account).filter(
                Account.status == 'passed'
            ).order_by(Account.updated_at.desc()).limit(5).all()
            
            for account in recent_passes:
                recent_activity.append({
                    "type": "account_pass",
                    "user_id": account.user_id,
                    "username": account.user.username,
                    "timestamp": account.updated_at,
                    "details": f"Account {account.id} passed challenge"
                })
            
            return AdminDashboardMetrics(
                user_metrics=user_metrics,
                account_metrics=account_metrics,
                trading_metrics=trading_metrics,
                financial_metrics=financial_metrics,
                system_metrics=system_metrics,
                recent_activity=recent_activity
            )
            
        except Exception as e:
            logger.error(f"Error getting admin dashboard metrics: {str(e)}")
            raise

    @staticmethod
    def manage_user(db: Session, action_data: UserManagementAction) -> dict:
        """Perform user management actions"""
        try:
            user = db.query(User).filter(User.id == action_data.user_id).first()
            if not user:
                raise ValueError(f"User {action_data.user_id} not found")
            
            action = action_data.action.lower()
            result = {
                "user_id": str(user.id),
                "username": user.username,
                "action": action,
                "success": True,
                "message": ""
            }
            
            if action == "suspend":
                user.is_suspended = True
                user.suspension_reason = action_data.reason
                result["message"] = f"User {user.username} suspended"
                
            elif action == "unsuspend":
                user.is_suspended = False
                user.suspension_reason = None
                result["message"] = f"User {user.username} unsuspended"
                
            elif action == "delete":
                # Soft delete - mark as deleted rather than actually delete
                user.is_active = False
                user.email = f"deleted_{user.id}@deleted.com"
                user.username = f"deleted_{user.id}"
                result["message"] = f"User {user.username} deleted"
                
            elif action == "reset_password":
                # Generate new temporary password
                temp_password = str(uuid.uuid4())[:12]
                user.hashed_password = get_password_hash(temp_password)
                result["message"] = f"Password reset for user {user.username}. New temporary password: {temp_password}"
                result["temp_password"] = temp_password
                
            else:
                raise ValueError(f"Invalid action: {action}")
            
            db.commit()
            logger.info(f"User management action performed: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error performing user management action: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def manage_account(db: Session, action_data: AccountManagementAction) -> dict:
        """Perform account management actions"""
        try:
            account = db.query(Account).filter(Account.id == action_data.account_id).first()
            if not account:
                raise ValueError(f"Account {action_data.account_id} not found")
            
            action = action_data.action.lower()
            result = {
                "account_id": str(account.id),
                "user_id": str(account.user_id),
                "username": account.user.username,
                "action": action,
                "success": True,
                "message": ""
            }
            
            if action == "review":
                # Mark account for manual review
                account.status = "pending"
                result["message"] = f"Account {account.id} marked for review"
                
            elif action == "reset":
                # Reset account to initial state
                account.status = "active"
                account.current_balance = account.initial_balance
                account.max_balance = account.initial_balance
                account.total_trades = 0
                account.total_profit = Decimal('0')
                account.total_loss = Decimal('0')
                result["message"] = f"Account {account.id} reset to initial state"
                
            elif action == "recalculate":
                # Recalculate account metrics from trades
                trades = db.query(Trade).filter(Trade.account_id == account.id).all()
                
                account.total_trades = len(trades)
                account.total_profit = sum(t.profit for t in trades if t.profit and t.profit > 0) or Decimal('0')
                account.total_loss = abs(sum(t.profit for t in trades if t.profit and t.profit < 0) or Decimal('0'))
                
                if trades:
                    account.current_balance = account.initial_balance + sum(t.profit for t in trades if t.profit) or Decimal('0')
                    account.max_balance = max(account.initial_balance, account.current_balance)
                
                result["message"] = f"Account {account.id} metrics recalculated"
                
            else:
                raise ValueError(f"Invalid action: {action}")
            
            db.commit()
            logger.info(f"Account management action performed: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error performing account management action: {str(e)}")
            db.rollback()
            raise

    @staticmethod
    def generate_revenue_report(db: Session, report_request: RevenueReportRequest) -> RevenueReportResponse:
        """Generate detailed revenue report"""
        try:
            # Query payments in date range
            payments_query = db.query(Payment).filter(
                Payment.created_at >= report_request.start_date,
                Payment.created_at <= report_request.end_date,
                Payment.status == 'completed'
            )
            
            payments = payments_query.all()
            
            # Calculate aggregates
            total_revenue = sum(p.amount for p in payments) or Decimal('0')
            new_revenue = sum(p.amount for p in payments if p.payment_type == 'challenge_purchase') or Decimal('0')
            processed_revenue = sum(p.amount for p in payments if p.payment_type == 'account_upgrade') or Decimal('0')
            refund_amount = sum(p.amount for p in payments if p.payment_type == 'refund') or Decimal('0')
            
            net_revenue = total_revenue - refund_amount
            transaction_count = len(payments)
            
            # Generate period string
            if report_request.group_by == "day":
                period = f"{report_request.start_date.date()} to {report_request.end_date.date()}"
            elif report_request.group_by == "week":
                period = f"Week of {report_request.start_date.date()}"
            else:  # month
                period = f"{report_request.start_date.strftime('%B %Y')}"
            
            # Generate details if requested
            details = None
            if report_request.include_details:
                details = []
                for payment in payments:
                    details.append({
                        "payment_id": str(payment.id),
                        "user_id": str(payment.user_id),
                        "username": payment.user.username,
                        "amount": float(payment.amount),
                        "payment_type": payment.payment_type,
                        "created_at": payment.created_at
                    })
            
            return RevenueReportResponse(
                period=period,
                total_revenue=total_revenue,
                new_revenue=new_revenue,
                processed_revenue=processed_revenue,
                refund_amount=refund_amount,
                net_revenue=net_revenue,
                transaction_count=transaction_count,
                details=details
            )
            
        except Exception as e:
            logger.error(f"Error generating revenue report: {str(e)}")
            raise

    @staticmethod
    def get_system_status(db: Session) -> dict:
        """Get overall system status and health metrics"""
        try:
            # Database health
            try:
                db.execute("SELECT 1")
                db_health = "healthy"
            except Exception:
                db_health = "unhealthy"
            
            # Recent job execution status
            recent_jobs = db.query(JobExecutionLog).order_by(
                JobExecutionLog.started_at.desc()
            ).limit(10).all()
            
            job_success_rate = 100
            if recent_jobs:
                successful_jobs = len([j for j in recent_jobs if j.status == 'completed'])
                job_success_rate = (successful_jobs / len(recent_jobs)) * 100
            
            # System metrics
            uptime = "100%"  # Would come from system monitoring
            response_time = "50ms"  # Would come from monitoring
            
            return {
                "status": "operational" if db_health == "healthy" and job_success_rate > 90 else "degraded",
                "database": db_health,
                "job_success_rate": job_success_rate,
                "uptime": uptime,
                "response_time": response_time,
                "last_updated": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "last_updated": datetime.utcnow()
            }

# Import JobExecutionLog for system status
from app.models.phase4.risk import JobExecutionLog