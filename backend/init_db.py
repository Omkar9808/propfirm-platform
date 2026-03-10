from sqlalchemy.orm import Session
from app.db.base import engine, SessionLocal
from app.db.seed import init_roles, init_admin_user, init_base_challenge
import sys

def init_db():
    """Initialize the database with default data"""
    db = SessionLocal()
    try:
        print("Initializing database...")
        
        # Create tables
        from app.db.base import Base
        from app import models  # Import to register models
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        
        # Initialize roles
        init_roles(db)
        
        # Initialize admin user
        init_admin_user(db)
        
        # Initialize base challenge
        init_base_challenge(db)
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()