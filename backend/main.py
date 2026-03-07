from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import engine
from backend.models.base import Base
from backend.routers import products, orders, reconciliations, platforms
from backend.scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化資料表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 啟動背景排程器
    start_scheduler()
    
    yield
    
    # 關閉背景排程器與資料庫連線
    shutdown_scheduler()
    await engine.dispose()

app = FastAPI(title="多平台商品與訂單管理系統 API", lifespan=lifespan)

# 設定 CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://goods-manager-frontend-164815154526.asia-east1.run.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(reconciliations.router, prefix="/api/reconciliations", tags=["Reconciliations"])
app.include_router(platforms.router, prefix="/api/platforms", tags=["Platforms"])

@app.get("/")
async def root():
    return {"message": "API Running"}
