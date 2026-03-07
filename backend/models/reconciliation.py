from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from .base import Base

class Reconciliation(Base):
    __tablename__ = "reconciliations"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True, nullable=False)
    settlement_date = Column(Date, index=True, nullable=False)
    
    total_revenue = Column(Float, nullable=False, default=0.0)
    platform_fee = Column(Float, nullable=False, default=0.0)
    shipping_fee = Column(Float, nullable=False, default=0.0)
    net_income = Column(Float, nullable=False, default=0.0)
    
    status = Column(String, default="pending") # pending, settled
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
