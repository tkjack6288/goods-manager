from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from backend.database import get_db
from backend.models.reconciliation import Reconciliation
from backend.schemas.reconciliation import ReconciliationResponse, ReconciliationCreate

router = APIRouter()

@router.get("/", response_model=List[ReconciliationResponse])
async def list_reconciliations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reconciliation).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=ReconciliationResponse)
async def create_reconciliation(recon_in: ReconciliationCreate, db: AsyncSession = Depends(get_db)):
    db_recon = Reconciliation(**recon_in.model_dump())
    db.add(db_recon)
    await db.commit()
    await db.refresh(db_recon)
    return db_recon
