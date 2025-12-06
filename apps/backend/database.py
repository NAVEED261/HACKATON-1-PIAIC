import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Lazy initialization for serverless
_engine = None
_SessionLocal = None

def get_database_engine():
    """Lazy initialization of database engine"""
    global _engine
    if _engine is None:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set")
        _engine = create_engine(DATABASE_URL)
    return _engine

def get_session_local():
    """Lazy initialization of session maker"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_database_engine())
    return _SessionLocal

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    learning_preferences = Column(Text, nullable=True)  # JSON string or similar
    hardware_software_background = Column(Text, nullable=True) # JSON string or similar

def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

# This will create tables in the database (for initial setup, Alembic will manage migrations)
def create_db_tables():
    Base.metadata.create_all(bind=get_database_engine())
