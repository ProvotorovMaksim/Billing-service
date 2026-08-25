from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from db_provider import get_db, get_tariff
from models import Subscription, Tariff, SubscriptionStatus
from schemas import Subscription as SubscriptionCreate, Subscription as SubscriptionResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(
    sub_data: SubscriptionCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Создать новую подписку для пользователя"""
    # 1. Проверяем существование тарифа
    tariff = await get_tariff(sub_data.tariff_id, db)
    if not tariff:
        raise HTTPException(status_code=404, detail="Указанный тариф не найден")
    
    # 2. Проверяем, есть ли уже активная подписка у этого пользователя
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == sub_data.user_id,
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="У пользователя уже есть активная подписка")
    
    # 3. Создаем подписку
    start_date = datetime.now()
    end_date = start_date + timedelta(days=tariff.period_days)
    
    new_subscription = Subscription(
        user_id=sub_data.user_id,
        tariff_id=sub_data.tariff_id,
        status=SubscriptionStatus.PENDING,
        start_date=start_date,
        end_date=end_date
    )
    
    db.add(new_subscription)
    await db.commit()
    await db.refresh(new_subscription)
    
    return new_subscription

@router.get("/user/{user_id}", response_model=SubscriptionResponse)
async def get_user_subscription(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получить текущую активную подписку пользователя"""
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Активная подписка не найдена")
    
    return subscription

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(subscription_id: int, db: AsyncSession = Depends(get_db)):
    """Получить детали конкретной подписки"""
    subscription = await db.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return subscription
