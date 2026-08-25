from fastapi import APIRouter as Router, Depends, HTTPException
from db_provider import get_db, AsyncSession, get_subscription, get_tariff, add_payment, set_payment_id, payment_callback
from schemas import PaymentRequest, PaymentConfirmationRequest, Payment
from models import PaymentStatus
from yookassa_service import YookassaService
from kafka_producer import publish_payment_success
from logging import getLogger

logger = getLogger("payments")
logger.setLevel("INFO")

yookassa = YookassaService()

router = Router()

@router.post("/create/")
async def create_payment(
    payment_data: PaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    subscription = await get_subscription(payment_data.subscription_id, db)

    tariff = await get_tariff(subscription.tariff_id, db)

    payment = Payment(
        subscription_id=payment_data.subscription_id,
        user_id=payment_data.user_id,
        amount=payment_data.amount,
        status=PaymentStatus.PENDING
    )

    await add_payment(payment, db)

    yookassa_result = yookassa.create_payment(
        amount=payment_data.amount,
        description=f"Оплата подписки {tariff.name}",
        order_id=payment_data.order_id
    )

    await set_payment_id(payment, yookassa_result, db)

    return {
        "order_id": payment_data.order_id,
        "confirmation_url": yookassa_result["confirmation_url"]
    }

@router.post("/webhook")
async def yookassa_webhook(
    confirmation: PaymentConfirmationRequest,
    db: AsyncSession = Depends(get_db)
):
    if confirmation.event != "payment.succeded":
        return {"status": "ignored"}

    payment = await payment_callback(PaymentConfirmationRequest.payment_id, db)

    if payment is None:
        logger.error("payment is null")
        raise

    publish_payment_success(payment)

    return {
        "status": "success"
    }