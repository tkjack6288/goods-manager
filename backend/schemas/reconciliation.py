from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ReconciliationBase(BaseModel):
    platform: str
    settlement_date: date
    total_revenue: float
    platform_fee: float
    shipping_fee: float
    net_income: float
    status: str = "pending"

class ReconciliationCreate(ReconciliationBase):
    pass

class ReconciliationResponse(ReconciliationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
