from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID

class CertificateCreate(BaseModel):
    account_id: UUID
    certificate_type: str
    title: str
    description: str
    certificate_data: Dict
    expires_in_days: Optional[int] = None

class CertificateResponse(BaseModel):
    id: UUID
    user_id: UUID
    account_id: UUID
    certificate_type: str
    title: str
    description: Optional[str]
    certificate_data: Optional[str]
    issued_at: datetime
    expires_at: Optional[datetime]
    is_verified: bool
    verification_code: Optional[str]
    template_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CertificateStats(BaseModel):
    total_certificates: int
    verified_certificates: int
    unverified_certificates: int
    expired_certificates: int