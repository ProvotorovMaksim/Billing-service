from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
import enum

class Base(DeclarativeBase):
    pass

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"

class Tariff(Base):
    __tablename__ = "tariffs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    period_days: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    tariff_id: Mapped[int] = mapped_column(Integer, ForeignKey("tariffs.id"))
    status: Mapped[SubscriptionStatus] = mapped_column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    tariff = relationship("Tariff")
    payments = relationship("Payment", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscriptions.id"))
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    yookassa_payment_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    subscription = relationship("Subscription", back_populates="payments")
