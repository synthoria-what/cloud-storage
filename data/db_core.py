from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


# engine = create_async_engine("postgres+asyncpg://postgres:pass@localhost:5432/cloud_storage_db")
engine = create_async_engine("sqlite+aiosqlite:///cloud_storage.db")
local_session = async_sessionmaker(bind=engine)

class Base(DeclarativeBase): pass


async def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)