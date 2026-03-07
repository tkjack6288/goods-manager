from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio
from datetime import datetime, timezone
import uuid

from backend.services.momo_service import MomoService
from backend.services.modianplus_service import ModianPlusService
from backend.services.shopee_service import ShopeeService
from backend.database import async_session_maker
from backend.models.product import Product
from backend.models.order import Order
from sqlalchemy import select

router = APIRouter()

async def save_products(products_data):
    if not products_data: return
    async with async_session_maker() as session:
        for item in products_data:
            sku = item.get("sku", "").strip()
            name = item.get("name", "").strip()
            if not name: continue
            
            try:
                price = float(item.get("price", 0))
            except ValueError:
                price = 0.0
                
            try:
                stock = int(item.get("stock", 0))
            except ValueError:
                stock = 0
                
            platform = item.get("platform")
            
            # 優先用 SKU 找，若無再用品名尋找
            if sku:
                stmt = select(Product).filter(Product.sku == sku)
            else:
                stmt = select(Product).filter(Product.name == name)
                
            result = await session.execute(stmt)
            db_product = result.scalars().first()
            
            if not db_product:
                new_sku = sku if sku else f"SKU-{str(uuid.uuid4()).split('-')[0].upper()}"
                db_product = Product(
                    name=name,
                    sku=new_sku,
                    price=price,
                    stock=stock
                )
                session.add(db_product)
                await session.flush()
                
            # 標記平台屬性
            if platform == "Momo":
                db_product.momo_active = True
            elif platform == "mo店+":
                db_product.modianplus_active = True
            elif platform == "Shopee":
                db_product.shopee_active = True
                
        await session.commit()

async def save_orders(orders_data):
    if not orders_data: return
    async with async_session_maker() as session:
        for item in orders_data:
            platform = item.get("platform")
            order_id = item.get("order_id", "").strip()
            if not order_id: continue
            
            stmt = select(Order).filter_by(platform=platform, platform_order_id=order_id)
            result = await session.execute(stmt)
            db_order = result.scalars().first()
            
            status = item.get("status", "pending")
            try:
                amount = float(item.get("amount", 0))
            except ValueError:
                amount = 0.0
            customer = item.get("customer", "")
            
            if not db_order:
                db_order = Order(
                    platform=platform,
                    platform_order_id=order_id,
                    status=status,
                    total_amount=amount,
                    order_date=datetime.now(timezone.utc),
                    customer_info={"name": customer} if customer else {},
                    platform_details=item.get("platform_details")
                )
                session.add(db_order)
            else:
                # 訂單已存在，不再執行任何更新，避免覆寫 GCP DB 內的目前狀態
                continue
                
        await session.commit()

async def run_sync_all_products():
    """背景執行全部平台的商品抓取與聯動更新"""
    momo = MomoService(headless=False)
    modian = ModianPlusService(headless=False)
    shopee = ShopeeService(headless=False)
    
    try:
        results = await asyncio.gather(
            momo.sync_products(),
            modian.sync_products(),
            shopee.sync_products(),
            return_exceptions=True
        )
        for result in results:
            if isinstance(result, list):
                await save_products(result)
    except Exception as e:
        print(f"背景同步商品時發生錯誤: {e}")

async def run_sync_all_orders(platform: str = None):
    """背景執行全部或指定平台的訂單抓取與聯動更新"""
    tasks = []
    
    if not platform or platform.lower() == "momo":
        momo = MomoService(headless=False)
        tasks.append(momo.fetch_orders())
        
    if not platform or platform.lower() == "modian":
        modian = ModianPlusService(headless=False)
        tasks.append(modian.fetch_orders())
        
    if not platform or platform.lower() == "shopee":
        shopee = ShopeeService(headless=False)
        tasks.append(shopee.fetch_orders())
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                await save_orders(result)
    except Exception as e:
        print(f"背景同步訂單時發生錯誤: {e}")

@router.post("/sync/products")
async def sync_products(background_tasks: BackgroundTasks):
    """觸發全平台商品同步任務至背景執行"""
    background_tasks.add_task(run_sync_all_products)
    return {"status": "ok", "message": "全平台商品同步任務已於背景啟動"}

@router.post("/sync/orders")
async def sync_orders(background_tasks: BackgroundTasks, platform: str = None):
    """觸發全平台或特定平台的訂單同步任務至背景執行"""
    background_tasks.add_task(run_sync_all_orders, platform)
    msg = f"{platform} 平台訂單同步任務已於背景啟動" if platform else "全平台訂單同步任務已於背景啟動"
    return {"status": "ok", "message": msg}
