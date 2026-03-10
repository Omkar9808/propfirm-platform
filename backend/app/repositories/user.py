from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role, RoleEnum
from app.schemas.auth import UserCreate
from app.utils.security import get_password_hash
from uuid import UUID

class UserRepository:
    """Repository for user-related database operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate, role_id: UUID) -> User:
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            role_id=role_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user_last_login(db: Session, user: User, ip_address: str = None):
        from sqlalchemy import func
        user.last_login_at = func.now()
        user.last_login_ip = ip_address
        db.commit()
        db.refresh(user)
        return user