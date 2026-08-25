from yookassa import Configuration, Payment
from settings import settings
import uuid

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

class YookassaService:
    @staticmethod
    def create_payment(amount: float, description: str, order_id: str) -> dict:
        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_RETURN_URL
            },
            "capture": True,
            "description": description,
            "metadata": {
                "order_id": order_id
            }
        }, uuid.uuid4())

        assert payment.confirmation is not None
        return {
            "payment_id": payment.id,
            "confirmation_url": payment.confirmation.confirmation_url
        }

    @staticmethod
    def get_payment_info(payment_id: str):
        payment = Payment.find_one(payment_id)
        return {
            "id": payment.id,
            "status": payment.status,
            "amount": payment.amount,
            "paid": payment.paid
        }