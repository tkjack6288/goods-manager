from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    stock: int = 0
    momo_product_id: Optional[str] = None
    momo_active: bool = False
    modianplus_product_id: Optional[str] = None
    modianplus_active: bool = False
    shopee_product_id: Optional[str] = None
    shopee_active: bool = False
    attributes: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
