from sqlalchemy.orm import Session
from app.models.phase4.risk import Violation, AccountStatusHistory, JobExecutionLog
from app.models.phase2.account import Account
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timedelta
import pytz

class ViolationRepository:
    """Repository for violation-related database operations"""
    
    @staticmethod
    def get_violation_by_id(db: Session, violation_id: UUID) -> Optional[Violation]:
        return db.query(Violation).filter(Violation.id == violation_id).first()
    
    @staticmethod
    def get_violations_by_account(db: Session, account_id: UUID, 
                                include_resolved: bool = False) -> List[Violation]:
        query = db.query(Violation).filter(Violation.account_id == account_id)
        if not include_resolved:
            query = query.filter(Violation.is_resolved == False)
        return query.order_by(Violation.created_at.desc()).all()
    
    @staticmethod
    def get_active_violations_by_account(db: Session, account_id: UUID) -> List[Violation]:
        return db.query(Violation).filter(
            Violation.account_id == account_id,
            Violation.is_resolved == False
        ).all()
    
    @staticmethod
    def create_violation(db: Session, violation_data: dict) -> Violation:
        db_violation = Violation(**violation_data)
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
        return db_violation
    
    @staticmethod
    def resolve_violation(db: Session, violation_id: UUID, 
                         resolved_by: UUID, resolution_notes: str = None) -> Violation:
        violation = ViolationRepository.get_violation_by_id(db, violation_id)
        if violation and not violation.is_resolved:
            violation.is_resolved = True
            violation.resolved_at = datetime.now(pytz.UTC)
            violation.resolved_by = resolved_by
            violation.resolution_notes = resolution_notes
            db.commit()
            db.refresh(violation)
        return violation
    
    @staticmethod
    def get_violation_summary(db: Session, account_id: UUID) -> dict:
        """Get violation statistics for an account"""
        total_violations = db.query(Violation).filter(
            Violation.account_id == account_id
        ).count()
        
        active_violations = db.query(Violation).filter(
            Violation.account_id == account_id,
            Violation.is_resolved == False
        ).count()
        
        resolved_violations = total_violations - active_violations
        
        # Get most recent violation types
        recent_violations = db.query(Violation.violation_type).filter(
            Violation.account_id == account_id
        ).order_by(Violation.created_at.desc()).limit(5).all()
        
        return {
            "total_violations": total_violations,
            "active_violations": active_violations,
            "resolved_violations": resolved_violations,
            "recent_violation_types": [v[0] for v in recent_violations]
        }

class AccountStatusHistoryRepository:
    """Repository for account status history operations"""
    
    @staticmethod
    def get_status_history_by_id(db: Session, history_id: UUID) -> Optional[AccountStatusHistory]:
        return db.query(AccountStatusHistory).filter(AccountStatusHistory.id == history_id).first()
    
    @staticmethod
    def get_status_history_by_account(db: Session, account_id: UUID, 
                                    limit: int = 100) -> List[AccountStatusHistory]:
        return db.query(AccountStatusHistory).filter(
            AccountStatusHistory.account_id == account_id
        ).order_by(AccountStatusHistory.changed_at.desc()).limit(limit).all()
    
    @staticmethod
    def create_status_change(db: Session, history_data: dict) -> AccountStatusHistory:
        db_history = AccountStatusHistory(**history_data)
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return db_history
    
    @staticmethod
    def get_account_current_status(db: Session, account_id: UUID) -> Optional[str]:
        """Get the current status of an account"""
        latest_change = db.query(AccountStatusHistory).filter(
            AccountStatusHistory.account_id == account_id
        ).order_by(AccountStatusHistory.changed_at.desc()).first()
        
        return latest_change.to_status if latest_change else None
    
    @staticmethod
    def get_status_timeline(db: Session, account_id: UUID, 
                          days: int = 30) -> List[AccountStatusHistory]:
        """Get status changes for the last N days"""
        cutoff_date = datetime.now(pytz.UTC) - timedelta(days=days)
        return db.query(AccountStatusHistory).filter(
            AccountStatusHistory.account_id == account_id,
            AccountStatusHistory.changed_at >= cutoff_date
        ).order_by(AccountStatusHistory.changed_at.desc()).all()

class JobExecutionLogRepository:
    """Repository for job execution logging operations"""
    
    @staticmethod
    def get_job_log_by_id(db: Session, log_id: UUID) -> Optional[JobExecutionLog]:
        return db.query(JobExecutionLog).filter(JobExecutionLog.id == log_id).first()
    
    @staticmethod
    def get_job_logs(db: Session, job_type: str = None, 
                    status: str = None, limit: int = 100) -> List[JobExecutionLog]:
        query = db.query(JobExecutionLog)
        
        if job_type:
            query = query.filter(JobExecutionLog.job_type == job_type)
        if status:
            query = query.filter(JobExecutionLog.status == status)
            
        return query.order_by(JobExecutionLog.started_at.desc()).limit(limit).all()
    
    @staticmethod
    def create_job_log(db: Session, log_data: dict) -> JobExecutionLog:
        db_log = JobExecutionLog(**log_data)
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def update_job_log(db: Session, log_id: UUID, update_data: dict) -> JobExecutionLog:
        log = JobExecutionLogRepository.get_job_log_by_id(db, log_id)
        if log:
            for key, value in update_data.items():
                if value is not None:
                    setattr(log, key, value)
            db.commit()
            db.refresh(log)
        return log
    
    @staticmethod
    def get_recent_job_status(db: Session, job_name: str) -> Optional[JobExecutionLog]:
        """Get the most recent execution of a specific job"""
        return db.query(JobExecutionLog).filter(
            JobExecutionLog.job_name == job_name
        ).order_by(JobExecutionLog.started_at.desc()).first()
    
    @staticmethod
    def get_job_statistics(db: Session, job_type: str, hours: int = 24) -> dict:
        """Get execution statistics for a job type"""
        from datetime import timedelta
        cutoff_time = datetime.now(pytz.UTC) - timedelta(hours=hours)
        
        jobs = db.query(JobExecutionLog).filter(
            JobExecutionLog.job_type == job_type,
            JobExecutionLog.started_at >= cutoff_time
        ).all()
        
        total_executions = len(jobs)
        successful_executions = len([j for j in jobs if j.status == "success"])
        failed_executions = len([j for j in jobs if j.status == "failed"])
        
        avg_duration = sum(j.duration_ms or 0 for j in jobs) / len(jobs) if jobs else 0
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            "avg_duration_ms": avg_duration,
            "last_execution": jobs[0].started_at if jobs else None
        }