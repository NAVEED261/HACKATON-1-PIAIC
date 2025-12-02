import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    learning_preferences = Column(Text, nullable=True)  # JSON string or similar
    hardware_software_background = Column(Text, nullable=True) # JSON string or similar

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This will create tables in the database (for initial setup, Alembic will manage migrations)
def create_db_tables():
    Base.metadata.create_all(bind=engine)
