from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.seed import init_roles, init_admin_user

def init_database():
    """Initialize the database with default roles and admin user"""
    db = next(get_db())
    try:
        print("Initializing database...")
        init_roles(db)
        init_admin_user(db)
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()