from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.schemas.phase4 import (
    ViolationCreate, ViolationUpdate, ViolationResponse,
    AccountStatusHistoryCreate, AccountStatusHistoryResponse,
    JobExecutionLogCreate, JobExecutionLogResponse,
    RiskEvaluationResult, AccountRiskStatus, ManualAccountAction,
    RiskEngineSettings, RiskEngineStatus
)
from app.services.auth import AuthService
from app.services.phase4 import RiskEngineService
from app.models.user import User
from typing import List
from uuid import UUID
import time

router = APIRouter(prefix="/risk", tags=["risk"])

# Violation endpoints
@router.post("/violations", response_model=ViolationResponse, status_code=status.HTTP_201_CREATED)
async def create_violation(
    violation_data: ViolationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new violation record (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create violations"
        )
    
    from app.repositories.phase4 import ViolationRepository
    violation = ViolationRepository.create_violation(db, violation_data.model_dump())
    return ViolationResponse.model_validate(violation)

@router.put("/violations/{violation_id}", response_model=ViolationResponse)
async def resolve_violation(
    violation_id: str,
    violation_update: ViolationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Resolve a violation (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to resolve violations"
        )
    
    from app.repositories.phase4 import ViolationRepository
    from uuid import UUID
    
    violation = ViolationRepository.resolve_violation(
        db, UUID(violation_id), 
        current_user.id, 
        violation_update.resolution_notes
    )
    
    if not violation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Violation not found or already resolved"
        )
    
    return ViolationResponse.model_validate(violation)

@router.get("/violations/account/{account_id}", response_model=List[ViolationResponse])
async def get_account_violations(
    account_id: str,
    include_resolved: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get violations for a specific account"""
    from app.repositories.phase4 import ViolationRepository
    from app.repositories.phase2 import AccountRepository
    from uuid import UUID
    
    # Verify account ownership
    account = AccountRepository.get_account_by_id(db, UUID(account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    violations = ViolationRepository.get_violations_by_account(
        db, UUID(account_id), include_resolved
    )
    return [ViolationResponse.model_validate(v) for v in violations]

# Account status history endpoints
@router.get("/status-history/account/{account_id}", response_model=List[AccountStatusHistoryResponse])
async def get_account_status_history(
    account_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get status history for an account"""
    from app.repositories.phase4 import AccountStatusHistoryRepository
    from app.repositories.phase2 import AccountRepository
    from uuid import UUID
    
    # Verify account ownership
    account = AccountRepository.get_account_by_id(db, UUID(account_id))
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this account"
        )
    
    history = AccountStatusHistoryRepository.get_status_history_by_account(
        db, UUID(account_id), limit
    )
    return [AccountStatusHistoryResponse.model_validate(h) for h in history]

# Risk evaluation endpoints
@router.post("/risk/evaluate/{account_id}", response_model=RiskEvaluationResult)
async def evaluate_account_risk(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Evaluate risk for a specific account"""
    from uuid import UUID
    result = RiskEngineService.evaluate_account_risk(db, UUID(account_id))
    return result

@router.post("/risk/evaluate-all", response_model=dict)
async def evaluate_all_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Evaluate risk for all active accounts (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to run batch evaluations"
        )
    
    result = RiskEngineService.evaluate_all_active_accounts(db)
    return result

@router.get("/risk/status/{account_id}", response_model=AccountRiskStatus)
async def get_account_risk_status(
    account_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive risk status for an account"""
    from uuid import UUID
    status_info = RiskEngineService.get_account_risk_status(db, current_user, UUID(account_id))
    return status_info

# Manual account actions (admin only)
@router.post("/admin/account-action", response_model=dict)
async def manual_account_action(
    action_data: ManualAccountAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Perform manual account action (admin only)"""
    result = RiskEngineService.manual_account_action(db, current_user, action_data)
    return result

@router.post("/admin/account/{account_id}/pass", response_model=dict)
async def manually_pass_account(
    account_id: str,
    reason: str,
    notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Manually pass an account (admin only)"""
    from uuid import UUID
    action_data = ManualAccountAction(
        account_id=UUID(account_id),
        action="pass",
        reason=reason,
        notes=notes
    )
    result = RiskEngineService.manual_account_action(db, current_user, action_data)
    return result

@router.post("/admin/account/{account_id}/fail", response_model=dict)
async def manually_fail_account(
    account_id: str,
    reason: str,
    notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Manually fail an account (admin only)"""
    from uuid import UUID
    action_data = ManualAccountAction(
        account_id=UUID(account_id),
        action="fail",
        reason=reason,
        notes=notes
    )
    result = RiskEngineService.manual_account_action(db, current_user, action_data)
    return result

# Job execution log endpoints
@router.get("/jobs/logs", response_model=List[JobExecutionLogResponse])
async def get_job_execution_logs(
    job_type: str = None,
    status: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get job execution logs (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view job logs"
        )
    
    from app.repositories.phase4 import JobExecutionLogRepository
    logs = JobExecutionLogRepository.get_job_logs(db, job_type, status, limit)
    return [JobExecutionLogResponse.model_validate(log) for log in logs]

@router.get("/jobs/logs/{job_id}", response_model=JobExecutionLogResponse)
async def get_job_execution_log(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific job execution log (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view job logs"
        )
    
    from app.repositories.phase4 import JobExecutionLogRepository
    from uuid import UUID
    
    log = JobExecutionLogRepository.get_job_log_by_id(db, UUID(job_id))
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job log not found"
        )
    
    return JobExecutionLogResponse.model_validate(log)

@router.get("/jobs/statistics/{job_type}", response_model=dict)
async def get_job_statistics(
    job_type: str,
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get job execution statistics (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view job statistics"
        )
    
    from app.repositories.phase4 import JobExecutionLogRepository
    stats = JobExecutionLogRepository.get_job_statistics(db, job_type, hours)
    return stats

# Risk engine monitoring endpoints
@router.get("/admin/engine/status", response_model=RiskEngineStatus)
async def get_risk_engine_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get risk engine status and settings (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view engine status"
        )
    
    from app.repositories.phase4 import JobExecutionLogRepository
    
    # Get recent job execution
    recent_job = JobExecutionLogRepository.get_recent_job_status(db, "risk_evaluation_batch")
    
    # Default settings (would come from config in production)
    settings = RiskEngineSettings(
        evaluation_interval_minutes=60,
        max_daily_loss_percent=5.0,
        max_total_loss_percent=10.0,
        min_win_rate_percent=30.0,
        is_enabled=True,
        last_evaluation_time=recent_job.started_at if recent_job else None
    )
    
    return RiskEngineStatus(
        is_running=False,  # Would check actual worker status
        last_run_time=recent_job.started_at if recent_job else None,
        next_scheduled_run=None,  # Would calculate based on schedule
        accounts_evaluated=recent_job.accounts_processed if recent_job else 0,
        accounts_passed=recent_job.accounts_passed if recent_job else 0,
        accounts_failed=recent_job.accounts_failed if recent_job else 0,
        violations_detected=recent_job.violations_created if recent_job else 0,
        settings=settings
    )

@router.get("/admin/engine/settings", response_model=RiskEngineSettings)
async def get_risk_engine_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get risk engine settings (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view engine settings"
        )
    
    # Default settings (would come from database/config in production)
    return RiskEngineSettings(
        evaluation_interval_minutes=60,
        max_daily_loss_percent=5.0,
        max_total_loss_percent=10.0,
        min_win_rate_percent=30.0,
        is_enabled=True
    )

@router.put("/admin/engine/settings", response_model=RiskEngineSettings)
async def update_risk_engine_settings(
    settings: RiskEngineSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update risk engine settings (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update engine settings"
        )
    
    # In production, this would update database settings
    # For now, just return the provided settings
    return settings

# Trigger endpoints for testing
@router.post("/admin/trigger-evaluation", response_model=dict)
async def trigger_risk_evaluation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Manually trigger risk evaluation (admin only)"""
    if current_user.role.name not in ["super_admin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to trigger evaluations"
        )
    
    result = RiskEngineService.evaluate_all_active_accounts(db)
    return {
        "message": "Risk evaluation triggered successfully",
        "job_id": result["job_id"],
        "accounts_evaluated": result["evaluated_accounts"]
    }