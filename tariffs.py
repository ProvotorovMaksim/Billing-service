from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db_provider import get_db, get_tariff as get_tariff_from_bd
from models import Tariff
from schemas import Tariff as TariffCreate, Tariff as TariffResponse

router = APIRouter(prefix="/tariffs", tags=["tariffs"])

@router.get("/", response_model=list[TariffResponse])
async def get_all_tariffs(db: AsyncSession = Depends(get_db)):
    """Получить список всех доступных тарифов"""
    result = await db.execute(select(Tariff))
    return result.scalars().all()

@router.get("/{tariff_id}", response_model=TariffResponse)
async def get_tariff(tariff_id: int, db: AsyncSession = Depends(get_db)):
    """Получить конкретный тариф по ID"""
    tariff = await get_tariff_from_bd(tariff_id, db)
    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    return tariff

@router.post("/", response_model=TariffResponse, status_code=201)
async def create_tariff(tariff_data: TariffCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый тарифный план"""
    # Проверка на уникальность имени
    result = await db.execute(select(Tariff).where(Tariff.name == tariff_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Тариф с таким именем уже существует")
    
    new_tariff = Tariff(**tariff_data.model_dump())
    db.add(new_tariff)
    await db.commit()
    await db.refresh(new_tariff)
    
    return new_tariff
