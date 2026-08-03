from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    barcode: Optional[str] = Field(None, max_length=64)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    cost: Decimal = Field(..., ge=0, decimal_places=2)
    selling_price: Decimal = Field(..., ge=0, decimal_places=2)
    stock_quantity: int = Field(..., ge=0)
    supplier_id: Optional[int] = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    barcode: Optional[str] = Field(None, max_length=64)
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    cost: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    selling_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    product_id: int

    model_config = ConfigDict(from_attributes=True)