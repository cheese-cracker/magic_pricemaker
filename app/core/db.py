# Database connection
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal: AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
