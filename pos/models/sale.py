from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class Sale(Base):
    __tablename__ = "sale"

    sale_id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(30), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="sale")
    user = relationship("User", back_populates="sale")
    sale_items = relationship("SaleItem", back_populates="sale")
    payment = relationship("Payment", back_populates="sale",)
    receipt = relationship("Receipt", back_populates="sale")