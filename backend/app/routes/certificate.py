from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.certificate import CertificateService
from app.models.certificate import Certificate
from app.schemas.certificate import CertificateCreate, CertificateResponse, CertificateStats
from app.services.auth import AuthService
from app.models.user import User
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=CertificateResponse)
def generate_certificate(
    certificate_data: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Generate a new certificate"""
    # Verify user owns the account
    from app.models.account import Account
    account = db.query(Account).filter(
        Account.id == certificate_data.account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=403, detail="Not authorized to generate certificate for this account")
    
    certificate = CertificateService.generate_certificate(
        db=db,
        user_id=current_user.id,
        account_id=certificate_data.account_id,
        certificate_type=certificate_data.certificate_type,
        title=certificate_data.title,
        description=certificate_data.description,
        certificate_data=certificate_data.certificate_data,
        expires_in_days=certificate_data.expires_in_days
    )
    return certificate

@router.get("/me", response_model=List[CertificateResponse])
def get_my_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get all certificates for the current user"""
    return CertificateService.get_user_certificates(db, current_user.id, skip, limit)

@router.get("/account/{account_id}", response_model=List[CertificateResponse])
def get_account_certificates(
    account_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get all certificates for a specific account"""
    # Verify user owns the account
    from app.models.account import Account
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=403, detail="Not authorized to view certificates for this account")
    
    return CertificateService.get_account_certificates(db, account_id)

@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get a specific certificate by ID"""
    certificate = CertificateService.get_certificate(db, certificate_id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    if certificate.user_id != current_user.id and current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to view this certificate")
    return certificate

@router.post("/verify/{verification_code}")
def verify_certificate(
    verification_code: str,
    db: Session = Depends(get_db)
):
    """Verify a certificate by verification code"""
    certificate = CertificateService.verify_certificate(db, verification_code)
    if not certificate:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    return {"message": "Certificate verified successfully", "certificate": certificate}

@router.post("/{certificate_id}/revoke")
def revoke_certificate(
    certificate_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Revoke a certificate"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    certificate = CertificateService.revoke_certificate(db, certificate_id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {"message": "Certificate revoked successfully"}

@router.get("/admin/unverified", response_model=List[CertificateResponse])
def get_unverified_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get all unverified certificates for admin review"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return CertificateService.get_unverified_certificates(db, skip, limit)

@router.get("/types")
def get_certificate_types():
    """Get available certificate types"""
    return CertificateService.get_certificate_types()

@router.get("/admin/stats", response_model=CertificateStats)
def get_certificate_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    """Get certificate statistics"""
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return CertificateService.get_certificate_stats(db)