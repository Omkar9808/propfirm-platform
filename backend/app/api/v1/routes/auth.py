from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.services.auth import AuthService
from app.models.user import User

router = APIRouter()
security = HTTPBearer()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db = Depends(get_db)
):
    """Register a new user"""
    user = AuthService.register_user(db, user_data)
    # Convert SQLAlchemy model to Pydantic model
    from app.schemas.auth import UserResponse
    return UserResponse.model_validate(user)

@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    request: Request,
    db = Depends(get_db)
):
    """Login user and return access token"""
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    token = AuthService.authenticate_user(
        db, 
        login_data.email, 
        login_data.password,
        ip_address=client_ip,
        user_agent=user_agent
    )
    return token

@router.get("/me")
async def get_current_user_endpoint(
    credentials = Depends(security),
    db = Depends(get_db)
):
    """Get current authenticated user"""
    current_user = AuthService.get_current_user_from_token(db, credentials.credentials)
    # Convert SQLAlchemy model to Pydantic model
    from app.schemas.auth import UserResponse
    return UserResponse.model_validate(current_user)