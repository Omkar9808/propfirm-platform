from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.db.base import get_db
from app.models.user import User
from app.services.auth import AuthService

def get_current_active_user(
    db: Session = Depends(get_db),
    token: str = None
) -> User:
    """Get current active user from token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        user = AuthService.get_current_user_from_token(db, token)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )