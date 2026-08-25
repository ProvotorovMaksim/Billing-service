from typing import Any

from pydantic import BaseModel
from models import SubscriptionStatus, PaymentStatus
from datetime import datetime

class PaymentRequest(BaseModel):
    amount: float
    user_id: int
    order_id: str
    subscription_id: int

class PaymentConfirmationRequest(BaseModel):
    event: str
    payment_id: str

class Tariff(BaseModel):
    name: str
    price: float
    period_days: int
    description: str

class Subscription(BaseModel):
    user_id: int
    tariff_id: int
    status: SubscriptionStatus
    start_date: datetime
    end_date: datetime

class Payment(BaseModel):
    subscription_id: int
    user_id: int
    amount: float
    status: PaymentStatus
    yookassa_payment_id: str
    paid_at: datetime

    def __init__(
            self,
            subscription_id: int,
            user_id: int,
            amount: float,
            status: PaymentStatus
        ):
        self.subscription_id = subscription_id
        self.user_id = user_id
        self.amount = amount
        self.status = status

    