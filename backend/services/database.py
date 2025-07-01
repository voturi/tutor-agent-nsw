"""
TutorAgent MVP Database Service
"""

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logging import get_logger

logger = get_logger("database")

# Create database instance
database = Database(settings.DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Create metadata instance
metadata = MetaData()


async def get_database():
    """Dependency to get database connection."""
    async with database.transaction():
        yield database


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_tables():
    """Create database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise


async def drop_tables():
    """Drop database tables."""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Database tables dropped successfully")
    except Exception as e:
        logger.error(f"❌ Failed to drop database tables: {e}")
        raise
