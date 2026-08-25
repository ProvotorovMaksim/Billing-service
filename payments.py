from fastapi import APIRouter as Router, Depends
from db_provider import get_db, AsyncSession
from schemas import Payment, PaymentConfirmation
from models import PaymentStatus
from yookassa_service import YookassaService

yookassa = YookassaService()

router = Router()

@router.post("/create/")
async def create_payment(
    payment_data: Payment,
    db: AsyncSession = Depends(get_db)
):

    yookassa_result = yookassa.create_payment(
        amount=payment_data.amount,
        description=payment_data.description,
        order_id=payment_data.order_id
    )

    return {
        "order_id": payment_data.order_id,
        "confirmation_url": yookassa_result["confirmation_url"]
    }

@router.post("/webhook")
async def yookassa_webhook(
    confirmation: PaymentConfirmation,
    db: AsyncSession = Depends(get_db)
):
    # Заглушка
    return {
        "status": "success"
    }