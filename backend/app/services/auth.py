from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.base import get_db
from app.repositories.user import UserRepository
from app.repositories.role import RoleRepository
from app.repositories.audit import AuditRepository
from app.schemas.auth import UserCreate, UserLogin, Token, TokenData
from app.models.user import User
from app.models.role import RoleEnum
from app.utils.security import verify_password, create_access_token, verify_access_token
from datetime import timedelta
from app.core.config import settings
import uuid

security = HTTPBearer()

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        # Check if user already exists
        if UserRepository.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if UserRepository.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Get default trader role
        trader_role = RoleRepository.get_role_by_name(db, RoleEnum.TRADER)
        if not trader_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default role not found"
            )
        
        # Create user
        user = UserRepository.create_user(db, user_data, trader_role.id)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Token:
        # Get user
        user = UserRepository.get_user_by_email(db, email)
        if not user:
            # Log failed attempt
            AuditRepository.create_login_audit(
                db, 
                user_id=None,  # No user found
                ip_address=ip_address,
                user_agent=user_agent,
                status="failed",
                failure_reason="User not found"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            # Log failed attempt
            AuditRepository.create_login_audit(
                db,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                status="failed",
                failure_reason="Invalid password"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            AuditRepository.create_login_audit(
                db,
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent,
                status="failed",
                failure_reason="Account deactivated"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        UserRepository.update_user_last_login(db, user, ip_address)
        
        # Log successful login
        AuditRepository.create_login_audit(
            db,
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            status="success"
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "email": user.email,
                "role": user.role.name
            },
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token)
    
    @staticmethod
    def get_current_user_from_token(
        db: Session, 
        token: str
    ):
        payload = verify_access_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = UserRepository.get_user_by_id(db, uuid.UUID(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user

    @staticmethod
    def get_current_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        """Dependency to get current user from token"""
        return AuthService.get_current_user_from_token(db, credentials.credentials)
    
    @staticmethod
    def get_current_active_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        """Dependency to get current active user from token"""
        user = AuthService.get_current_user_from_token(db, credentials.credentials)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return user