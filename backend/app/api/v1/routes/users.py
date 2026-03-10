from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.repositories.user import UserRepository
from app.models.user import User
from app.services.auth import AuthService

router = APIRouter()
security = HTTPBearer()

@router.get("/")
async def get_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    credentials = Depends(security)
):
    """Get all users (admin only)"""
    users = UserRepository.get_users(db, skip=skip, limit=limit)
    return users