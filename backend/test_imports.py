import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    from app.main import app
    print("✓ Main app imports successfully")
    
    from app.db.base import Base, engine
    print("✓ Database imports successfully")
    
    from app.models.user import User
    print("✓ User model imports successfully")
    
    from app.schemas.auth import UserCreate, UserResponse
    print("✓ Schemas import successfully")
    
    from app.services.auth import AuthService
    print("✓ Auth service imports successfully")
    
    print("\nAll imports successful! The application is ready to run.")
    
except Exception as e:
    print(f"Error importing modules: {e}")
    import traceback
    traceback.print_exc()