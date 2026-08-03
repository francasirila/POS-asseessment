from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    contact_name = Column(String(100), nullable=False)
    phone_number = Column(String(30), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=False)
    supplied_at = Column(DateTime, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)

    products = relationship("Product", back_populates="supplier")