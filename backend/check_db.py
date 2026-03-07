import sys
import os
import asyncio

# Setup module path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import text
from backend.database import async_session_maker

async def check_orders():
    async with async_session_maker() as session:
        result = await session.execute(text('SELECT id, platform, platform_order_id, status, total_amount, platform_details FROM orders ORDER BY id DESC LIMIT 5'))
        rows = result.fetchall()
        print('Orders count:', len(rows))
        for r in rows:
            print(dict(r._mapping))

if __name__ == "__main__":
    asyncio.run(check_orders())
