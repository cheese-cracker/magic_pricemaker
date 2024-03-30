from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
# Database connection
from sqlalchemy import create_engine
from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
