import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class UserRole(str, enum.Enum):
    cashier = "cashier"
    manager = "manager"


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.cashier)

    sales = relationship("Sale", back_populates="user")