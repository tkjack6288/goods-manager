from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    
    # 各平台對應ID與上架狀態
    momo_product_id = Column(String, nullable=True)
    momo_active = Column(Boolean, default=False)
    
    modianplus_product_id = Column(String, nullable=True)
    modianplus_active = Column(Boolean, default=False)
    
    shopee_product_id = Column(String, nullable=True)
    shopee_active = Column(Boolean, default=False)
    
    # 彈性屬性紀錄 (規格、品牌等)
    attributes = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
