from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=150)
    contact_name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    address: str = Field(..., min_length=1, max_length=2000)
    supplied_at: datetime


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=150)
    contact_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=1, max_length=2000)
    supplied_at: Optional[datetime] = None


class SupplierResponse(SupplierBase):
    supplier_id: int

    model_config = ConfigDict(from_attributes=True)