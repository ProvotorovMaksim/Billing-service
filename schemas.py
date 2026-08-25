from pydantic import BaseModel

class Payment(BaseModel):
    amount: float
    description: str
    order_id: str

class PaymentConfirmation(BaseModel):
    pass