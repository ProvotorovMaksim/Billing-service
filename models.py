from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from db_provider import Base
from datetime import datetime
import enum

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"

class Tariff(Base):
    __tablename__ = "tariffs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    period_days = Column(Integer)  # например, 30 для месячной подписки
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # ID из auth-service
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    
    tariff = relationship("Tariff")
    payments = relationship("Payment", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    yookassa_payment_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    
    subscription = relationship("Subscription", back_populates="payments")
