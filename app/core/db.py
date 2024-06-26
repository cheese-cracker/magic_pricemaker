# Database connection
from app.core.config import settings
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal: AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


async def async_set_db():
    async with engine.begin() as conn:
        tables = await conn.run_sync( lambda sync_conn: inspect(sync_conn).get_table_names())
        if not len(tables):
            await conn.run_sync(Base.metadata.create_all)