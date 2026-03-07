from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_sku: str
    product_name: str
    quantity: int
    unit_price: float
    platform_details: Optional[Dict[str, Any]] = None

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    platform: str
    platform_order_id: str
    status: str
    total_amount: float
    customer_info: Optional[Dict[str, Any]] = None
    shipping_info: Optional[Dict[str, Any]] = None
    platform_details: Optional[Dict[str, Any]] = None
    order_date: datetime

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class OrderUpdateStatus(BaseModel):
    status: str

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
