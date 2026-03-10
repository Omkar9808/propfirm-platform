from sqlalchemy.orm import Session
from app.models.certificate import Certificate
from app.models.user import User
from app.models.phase2.account import Account
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import json

class CertificateService:
    @staticmethod
    def generate_certificate(
        db: Session,
        user_id: uuid.UUID,
        account_id: uuid.UUID,
        certificate_type: str,
        title: str,
        description: str,
        certificate_data: dict,
        expires_in_days: Optional[int] = None
    ) -> Certificate:
        """Generate a new certificate"""
        # Check if certificate already exists for this user/account/type combination
        existing_cert = db.query(Certificate).filter(
            Certificate.user_id == user_id,
            Certificate.account_id == account_id,
            Certificate.certificate_type == certificate_type
        ).first()
        
        if existing_cert:
            return existing_cert
        
        # Create expiration date if specified
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Generate unique verification code
        verification_code = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        
        certificate = Certificate(
            user_id=user_id,
            account_id=account_id,
            certificate_type=certificate_type,
            title=title,
            description=description,
            certificate_data=json.dumps(certificate_data),
            expires_at=expires_at,
            verification_code=verification_code
        )
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        return certificate

    @staticmethod
    def get_certificate(db: Session, certificate_id: uuid.UUID) -> Optional[Certificate]:
        """Get a specific certificate by ID"""
        return db.query(Certificate).filter(Certificate.id == certificate_id).first()

    @staticmethod
    def get_user_certificates(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Certificate]:
        """Get all certificates for a specific user"""
        return db.query(Certificate).filter(Certificate.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_account_certificates(db: Session, account_id: uuid.UUID) -> List[Certificate]:
        """Get all certificates for a specific account"""
        return db.query(Certificate).filter(Certificate.account_id == account_id).all()

    @staticmethod
    def verify_certificate(db: Session, verification_code: str) -> Optional[Certificate]:
        """Verify a certificate by verification code"""
        certificate = db.query(Certificate).filter(
            Certificate.verification_code == verification_code,
            Certificate.is_verified == False
        ).first()
        
        if not certificate:
            return None
        
        # Check if certificate is expired
        if certificate.expires_at and certificate.expires_at < datetime.utcnow():
            return None
        
        # Mark as verified
        certificate.is_verified = True
        db.commit()
        db.refresh(certificate)
        return certificate

    @staticmethod
    def revoke_certificate(db: Session, certificate_id: uuid.UUID) -> Optional[Certificate]:
        """Revoke a certificate"""
        certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
        if not certificate:
            return None
        
        certificate.is_verified = False
        db.commit()
        db.refresh(certificate)
        return certificate

    @staticmethod
    def get_certificate_types() -> dict:
        """Get available certificate types and their descriptions"""
        return {
            "profit_target_achieved": {
                "title": "Profit Target Achieved",
                "description": "Awarded when trader reaches profit target",
                "requires_verification": True
            },
            "risk_rule_passed": {
                "title": "Risk Rule Compliance",
                "description": "Awarded when trader passes all risk rules",
                "requires_verification": True
            },
            "consistency_achievement": {
                "title": "Consistency Achievement",
                "description": "Awarded for consistent trading performance",
                "requires_verification": False
            },
            "completion_certificate": {
                "title": "Challenge Completion",
                "description": "Awarded upon successful challenge completion",
                "requires_verification": True
            }
        }

    @staticmethod
    def get_unverified_certificates(db: Session, skip: int = 0, limit: int = 100) -> List[Certificate]:
        """Get all unverified certificates for admin review"""
        return db.query(Certificate).filter(
            Certificate.is_verified == False
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_certificate_stats(db: Session) -> dict:
        """Get certificate statistics"""
        total_certificates = db.query(Certificate).count()
        verified_certificates = db.query(Certificate).filter(Certificate.is_verified == True).count()
        unverified_certificates = db.query(Certificate).filter(Certificate.is_verified == False).count()
        expired_certificates = db.query(Certificate).filter(
            Certificate.expires_at < datetime.utcnow()
        ).count()
        
        return {
            "total_certificates": total_certificates,
            "verified_certificates": verified_certificates,
            "unverified_certificates": unverified_certificates,
            "expired_certificates": expired_certificates
        }