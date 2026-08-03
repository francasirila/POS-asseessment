from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, unique=True, index=True)
    receipt_number = Column(String(50), unique=True, nullable=False, index=True)
    issued_at = Column(DateTime, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    sale = relationship("Sale", back_populates="receipt")