from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from settings import settings
from models import PaymentStatus, SubscriptionStatus, Tariff, Subscription, Payment
from schemas import Payment as PaymentSchema
from logging import getLogger
from datetime import datetime, timedelta
from fastapi import HTTPException

logger = getLogger("db_provider")
logger.setLevel("INFO")

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

async def get_subscription(
        subscription_id: int,
        db: AsyncSession
) -> Subscription:
    """Возвращает SQLAlchemy модель, а не Pydantic схему"""
    subscription = await db.get(Subscription, subscription_id)
    if subscription is None:
        logger.error(f"Subscription with id {subscription_id} not found")
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

async def get_tariff(
        tariff_id: int,
        db: AsyncSession
) -> Tariff:
    """Возвращает SQLAlchemy модель"""
    tariff = await db.get(Tariff, tariff_id)
    if tariff is None:
        logger.error(f"Tariff with id {tariff_id} not found")
        raise HTTPException(status_code=404, detail="Tariff not found")
    return tariff

async def add_payment(
        payment: Payment,  # Принимаем словарь данных, а не Pydantic объект
        db: AsyncSession
) -> Payment:
    """Создает SQLAlchemy модель из словаря и сохраняет в БД"""
    # Создаем SQLAlchemy объект Payment, а не добавляем Pydantic схему
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment

async def set_payment_id(
        payment_id: int,
        yookassa_payment_id: str,
        db: AsyncSession
) -> Payment:
    """Обновляет ID платежа из ЮKassa"""
    payment = await db.get(Payment, payment_id)
    if payment is None:
        logger.error(f"Payment with id {payment_id} not found")
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.yookassa_payment_id = yookassa_payment_id
    await db.commit()
    await db.refresh(payment)
    return payment

async def activate_subscription(
        subscription_id: int,
        db: AsyncSession
) -> Subscription:
    """Активирует подписку и рассчитывает дату окончания"""
    subscription = await db.get(Subscription, subscription_id)
    if subscription is None:
        logger.error(f"Subscription with id {subscription_id} not found")
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.status = SubscriptionStatus.ACTIVE
    subscription.start_date = datetime.utcnow()

    tariff = await get_tariff(subscription.tariff_id, db)
    subscription.end_date = subscription.start_date + timedelta(days=tariff.period_days)

    await db.commit()
    await db.refresh(subscription)
    return subscription

async def payment_callback(
        yookassa_payment_id: str,
        db: AsyncSession
) -> Payment:
    """Обрабатывает успешный платеж от ЮKassa"""
    payment = await db.get(Payment, yookassa_payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = PaymentStatus.SUCCEEDED
    payment.paid_at = datetime.utcnow()

    await activate_subscription(payment.subscription_id, db)

    await db.commit()
    await db.refresh(payment)
    return payment
