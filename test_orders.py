import asyncio
from backend.database import async_session_maker
from backend.models.order import Order
from sqlalchemy import select, or_

async def main():
    async with async_session_maker() as session:
        search = "66030100836708"
        stmt = select(Order).filter(or_(
            Order.platform_order_id.ilike(f"%{search}%"),
            Order.customer_info.op('->>')('name').ilike(f"%{search}%")
        ))
        res = await session.execute(stmt)
        orders = res.scalars().all()
        print('SQLAlchemy filter results count:', len(orders))
        for o in orders:
            print(f"- ID: {o.platform_order_id}, Customer: {o.customer_info.get('name')}, Platform: {o.platform}")
        
        # print all orders count
        res_all = await session.execute(select(Order))
        all_orders = res_all.scalars().all()
        print('Total orders count:', len(all_orders))

asyncio.run(main())
