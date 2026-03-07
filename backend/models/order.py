from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True, nullable=False) # e.g. momo, shopee, modianplus
    platform_order_id = Column(String, unique=True, index=True, nullable=False)
    
    status = Column(String, nullable=False) # pending, shipped, completed, cancelled
    total_amount = Column(Float, nullable=False)
    
    customer_info = Column(JSON, nullable=True)
    shipping_info = Column(JSON, nullable=True)
    platform_details = Column(JSON, nullable=True) # 儲存特定平台的獨有欄位 (如 mo店+ 額外 28 欄)
    
    order_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_sku = Column(String, index=True, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    platform_details = Column(JSON, nullable=True) # 儲存特定平台的獨有商品明細 (如 mo店+ 原廠編號等)

    order = relationship("Order", back_populates="items")
