import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.routers.platforms import run_sync_all_products, run_sync_all_orders

logger = logging.getLogger(__name__)

# 初始化 AsyncIOScheduler
scheduler = AsyncIOScheduler()

def setup_scheduler():
    """設定定時任務 (Cron Jobs) 以同步庫存與訂單"""
    
    # 每 2 小時同步一次所有平台的商品及庫存
    scheduler.add_job(
        run_sync_all_products,
        'interval',
        hours=2,
        id='sync_all_products_job',
        replace_existing=True,
        name='全平台商品與庫存同步'
    )
    logger.info("已註冊商品同步任務 (每 2 小時)")

    # 每 30 分鐘同步一次最新訂單，確保儀表板資訊即時
    scheduler.add_job(
        run_sync_all_orders,
        'interval',
        minutes=30,
        id='sync_all_orders_job',
        replace_existing=True,
        name='全平台訂單同步'
    )
    logger.info("已註冊訂單同步任務 (每 30 分鐘)")

def start_scheduler():
    """啟動排程器"""
    if not scheduler.running:
        setup_scheduler()
        scheduler.start()
        logger.info("自動排程引擎 (Cron Jobs) 已成功啟動")

def shutdown_scheduler():
    """關閉排程器"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("自動排程引擎已關閉")
