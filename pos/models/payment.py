import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    mobile_money = "mobile_money"
    bank_transfer = "bank_transfer"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, unique=True, index=True)
    method = Column(Enum(PaymentMethod), nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.completed)
    transaction_reference = Column(String(100), nullable=False, unique=True, index=True)

    sale = relationship("Sale", back_populates="payment")