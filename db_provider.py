from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from settings import settings
from schemas import Tariff, Subscription, Payment
from models import PaymentStatus, SubscriptionStatus
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
    subscription = await db.get(Subscription, subscription_id)
    if subscription is None:
        logger.error("Subscription object from bd is null")
        raise
    return subscription

async def get_tariff(
        tariff_id: int,
        db:AsyncSession
) -> Tariff:
    tariff = await db.get(Tariff, tariff_id)
    if tariff is None:
            logger.error("Tariff object from bd is null")
            raise
    return tariff

async def add_payment(
        payment: Payment,
        db: AsyncSession
):
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

async def set_payment_id(
        payment: Payment,
        yookassa_result: dict,
        db: AsyncSession
):
    if yookassa_result.get("payment_id") is None:
        logger.error("Payment_id is null")
        raise
    payment.yookassa_payment_id = str(yookassa_result.get("payment_id"))

async def activate_subscription(
        subscription_id: int,
        db: AsyncSession
        ):
    subscription = await db.get(Subscription, subscription_id)
    if subscription is None:
        logger.error("Subscription object is null")
        raise
    subscription.status = SubscriptionStatus.ACTIVE
    subscription.start_date = datetime.now()

    tariff = await get_tariff(subscription.tariff_id, db)
    subscription.end_date = subscription.start_date + timedelta(days=tariff.period_days)

    await db.commit()

async def payment_callback(
        payment_id: str,
        db: AsyncSession
):
    payment = await db.get(Payment, payment_id)
    if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = PaymentStatus.SUCCEEDED
    payment.paid_at = datetime.now()

    await activate_subscription(payment.subscription_id, db)

    await db.commit()
    return payment