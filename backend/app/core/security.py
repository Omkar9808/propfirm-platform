from fastapi import HTTPException, status
from app.models.user import User

def verify_role(user: User, required_roles: list) -> bool:
    """Verify that user has one of the required roles"""
    if user.role.name not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return True

def get_password_hash(password: str) -> str:
    """Hash a password - using simple method for demonstration"""
    # In production, use proper password hashing like bcrypt
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()