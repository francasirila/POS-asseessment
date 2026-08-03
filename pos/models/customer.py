from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=True, index=True)
    phone_number = Column(String(30), unique=True, nullable=False, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.receipt_id"), nullable=True, index=True)

    sales = relationship("Sale", back_populates="customer")
    receipts = relationship("Receipt", back_populates="customer")