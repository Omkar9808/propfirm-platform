from sqlalchemy.orm import Session
from app.models.audit import LoginAuditLog, LoginStatusEnum
from uuid import UUID
import uuid

class AuditRepository:
    """Repository for audit log operations"""
    
    @staticmethod
    def create_login_audit(
        db: Session, 
        user_id: UUID, 
        ip_address: str, 
        user_agent: str,
        status: LoginStatusEnum,
        failure_reason: str = None,
        session_id: str = None
    ) -> LoginAuditLog:
        audit_log = LoginAuditLog(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            failure_reason=failure_reason,
            session_id=session_id
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log