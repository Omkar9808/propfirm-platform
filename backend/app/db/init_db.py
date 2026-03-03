from sqlalchemy import create_engine
from app.db.base import Base
from app.core.config import settings

def create_tables():
    """Create all tables defined in models"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()