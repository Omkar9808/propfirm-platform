from pydantic_settings import BaseSettings
from typing import List
import os
import urllib.parse

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Prop Firm Practice Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @property
    def DATABASE_URL(self) -> str:
        # Use psycopg2 driver with SSL mode for Supabase
        # Note: Password in .env should already be URL-encoded if it contains special chars
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:6543/{self.POSTGRES_DB}?sslmode=require"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()