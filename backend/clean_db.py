import sys
import os
import asyncio

# Setup module path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import text
from backend.database import async_session_maker

async def clean_orders():
    async with async_session_maker() as session:
        await session.execute(text("DELETE FROM orders WHERE platform = 'mo店+ (宅配)'"))
        await session.commit()
        print('Cleaned test orders')

if __name__ == "__main__":
    asyncio.run(clean_orders())
