import sys
import os
import asyncio

# 將外層目錄加入 PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from backend.core.config import settings

async def upgrade_db():
    engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    async with engine.begin() as conn:
        print("Checking orders table...")
        try:
            await conn.execute(text("ALTER TABLE orders ADD COLUMN platform_details JSON;"))
            print("Added platform_details to orders.")
        except Exception as e:
            print(f"Already exists or error in orders: {e}")
            
        print("Checking order_items table...")
        try:
            await conn.execute(text("ALTER TABLE order_items ADD COLUMN platform_details JSON;"))
            print("Added platform_details to order_items.")
        except Exception as e:
            print(f"Already exists or error in order_items: {e}")

if __name__ == "__main__":
    asyncio.run(upgrade_db())
