from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from backend.database import get_db
from backend.models.order import Order, OrderItem
from backend.schemas.order import OrderCreate, OrderUpdateStatus, OrderResponse

router = APIRouter()

from sqlalchemy import or_

@router.get("/", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), search: Optional[str] = None, platform: Optional[str] = None, status: Optional[str] = None):
    stmt = select(Order).options(selectinload(Order.items))
    
    if search:
        stmt = stmt.filter(or_(
            Order.platform_order_id.ilike(f"%{search}%"),
            Order.customer_info.op('->>')('name').ilike(f"%{search}%")
        ))
    if platform and platform != "全部平台":
        stmt = stmt.filter(Order.platform.ilike(f"%{platform}%"))
    if status and status != "全部狀態":
        stmt = stmt.filter(Order.status.ilike(f"%{status}%"))
        
    stmt = stmt.order_by(
        Order.platform_details.op('->>')('轉單日').asc(),
        Order.platform_order_id.asc()
    )
    
    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=OrderResponse)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    order_data = order_in.model_dump(exclude={"items"})
    db_order = Order(**order_data)
    
    for item_in in order_in.items:
        db_item = OrderItem(**item_in.model_dump())
        db_order.items.append(db_item)
        
    db.add(db_order)
    await db.commit()
    
    new_order_result = await db.execute(
        select(Order).options(selectinload(Order.items)).filter(Order.id == db_order.id)
    )
    return new_order_result.scalars().first()

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status_update: OrderUpdateStatus, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order).options(selectinload(Order.items)).filter(Order.id == order_id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order.status = status_update.status
    
    # 判斷是否需要同步運費或主訂單
    # 根據需求：若商品名稱為「運費」，將與相同訂單編號-001 同步。
    # 也可能會是主訂單切換狀態時，一併同步運費訂單。
    
    # 取得原始訂單編號前綴 (去除 -xxx 後綴)
    base_order_id = order.platform_order_id.split('-')[0] if '-' in order.platform_order_id else order.platform_order_id
    
    # 尋找所有相同前綴的訂單 (例如 123456, 123456-001 等)
    related_result = await db.execute(
        select(Order).filter(Order.platform_order_id.like(f"{base_order_id}%"))
    )
    related_orders = related_result.scalars().all()
    
    for rel_order in related_orders:
        if rel_order.id != order.id:
            rel_order.status = status_update.status
            
    await db.commit()
    await db.refresh(order)
    return order
