from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.core.config import settings

# 建立非同步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),
    future=True
)

# 建立非同步 Session 工廠
async_session_maker = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

async def get_db():
    """提供 FastAPI Dependency 注入的 Database Session 產生器"""
    async with async_session_maker() as session:
        yield session
