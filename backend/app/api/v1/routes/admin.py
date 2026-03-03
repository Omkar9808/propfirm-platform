from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.admin import AdminService
from app.schemas.phase5 import (
    AdminDashboardMetrics, UserManagementAction, AccountManagementAction,
    RevenueReportRequest, RevenueReportResponse
)
from app.core.security import verify_role

router = APIRouter(prefix="/admin", tags=["Admin"])

# Admin Dashboard Endpoints
@router.get("/dashboard", response_model=AdminDashboardMetrics)
async def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive admin dashboard metrics"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        dashboard = AdminService.get_dashboard_metrics(db)
        return dashboard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting admin dashboard: {str(e)}"
        )

@router.get("/system-status", response_model=dict)
async def get_system_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get system status and health metrics"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        status = AdminService.get_system_status(db)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting system status: {str(e)}"
        )

# User Management Endpoints
@router.post("/users/manage", response_model=dict)
async def manage_user(
    action_data: UserManagementAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Perform user management actions"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # Set performed_by
        action_data.performed_by = current_user.id
        result = AdminService.manage_user(db, action_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing user management action: {str(e)}"
        )

@router.get("/users/suspended", response_model=list)
async def get_suspended_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of suspended users"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        suspended_users = db.query(User).filter(User.is_suspended == True).all()
        return [
            {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
                "suspension_reason": user.suspension_reason,
                "suspended_at": user.updated_at
            }
            for user in suspended_users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting suspended users: {str(e)}"
        )

# Account Management Endpoints
@router.post("/accounts/manage", response_model=dict)
async def manage_account(
    action_data: AccountManagementAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Perform account management actions"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        # Set performed_by
        action_data.performed_by = current_user.id
        result = AdminService.manage_account(db, action_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing account management action: {str(e)}"
        )

@router.get("/accounts/pending", response_model=list)
async def get_pending_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of accounts pending review"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        pending_accounts = db.query(Account).filter(Account.status == 'pending').all()
        return [
            {
                "account_id": str(account.id),
                "user_id": str(account.user_id),
                "username": account.user.username,
                "created_at": account.created_at,
                "current_balance": float(account.current_balance or 0),
                "status": account.status
            }
            for account in pending_accounts
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting pending accounts: {str(e)}"
        )

# Revenue and Financial Endpoints
@router.post("/reports/revenue", response_model=RevenueReportResponse)
async def generate_revenue_report(
    report_request: RevenueReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate detailed revenue report"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        report = AdminService.generate_revenue_report(db, report_request)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating revenue report: {str(e)}"
        )

@router.get("/reports/daily-summary", response_model=dict)
async def get_daily_summary(
    date: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get daily business summary"""
    verify_role(current_user, ["admin", "super_admin"])
    
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.utcnow().date()
        
        # Get metrics for the day
        daily_metrics = db.query(PlatformMetrics).filter(
            func.date(PlatformMetrics.metric_date) == target_date
        ).first()
        
        if not daily_metrics:
            # Generate metrics if they don't exist
            daily_metrics = AnalyticsService.generate_platform_metrics(db, target_date)
        
        return {
            "date": daily_metrics.metric_date.date(),
            "new_users": daily_metrics.new_users,
            "new_accounts": daily_metrics.new_accounts,
            "total_trades": daily_metrics.total_trades,
            "total_volume": float(daily_metrics.total_volume),
            "total_revenue": float(daily_metrics.total_revenue),
            "active_accounts": daily_metrics.active_accounts,
            "passed_accounts": daily_metrics.passed_accounts,
            "failed_accounts": daily_metrics.failed_accounts
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting daily summary: {str(e)}"
        )

# System Administration Endpoints
@router.post("/system/maintenance", response_model=dict)
async def perform_maintenance(
    action: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Perform system maintenance actions"""
    verify_role(current_user, ["super_admin"])
    
    try:
        if action == "cleanup_old_data":
            # Clean up old audit logs (older than 90 days)
            cutoff_date = datetime.utcnow() - timedelta(days=90)
            deleted_count = db.query(LoginAuditLog).filter(
                LoginAuditLog.timestamp < cutoff_date
            ).delete()
            db.commit()
            
            return {
                "success": True,
                "action": "cleanup_old_data",
                "deleted_records": deleted_count,
                "message": f"Deleted {deleted_count} old audit log records"
            }
        
        elif action == "recalculate_all_metrics":
            # Recalculate all trader metrics
            result = AnalyticsService.calculate_all_trader_metrics(db)
            return {
                "success": True,
                "action": "recalculate_all_metrics",
                "message": "All trader metrics recalculated",
                "processed_traders": result["processed_traders"]
            }
        
        elif action == "update_leaderboard_cache":
            # Update leaderboard cache
            result = LeaderboardService.update_leaderboard_cache(db)
            return {
                "success": True,
                "action": "update_leaderboard_cache",
                "message": "Leaderboard cache updated",
                "total_entries": result["total_entries"]
            }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid maintenance action: {action}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing maintenance action: {str(e)}"
        )

# Import required models
from app.models.audit import LoginAuditLog
from app.models.phase2.account import Account
from app.services.phase5 import AnalyticsService
from app.services.leaderboard import LeaderboardService
from sqlalchemy import func