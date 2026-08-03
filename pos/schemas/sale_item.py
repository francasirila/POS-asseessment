from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SaleItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)


class SaleItemResponse(BaseModel):
    sale_item_id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)