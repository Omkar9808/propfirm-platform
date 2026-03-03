from sqlalchemy.orm import Session
from app.models.role import Role, RoleEnum
from uuid import UUID

class RoleRepository:
    """Repository for role-related database operations"""
    
    @staticmethod
    def get_role_by_id(db: Session, role_id: UUID) -> Role:
        return db.query(Role).filter(Role.id == role_id).first()
    
    @staticmethod
    def get_role_by_name(db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_roles(db: Session):
        return db.query(Role).all()
    
    @staticmethod
    def create_role(db: Session, name: RoleEnum, description: str = None) -> Role:
        db_role = Role(name=name, description=description)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role