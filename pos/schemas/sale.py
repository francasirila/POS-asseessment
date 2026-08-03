from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from pos.schemas.payment import PaymentRequest, PaymentResponse
from pos.schemas.receipt import ReceiptResponse
from pos.schemas.sale_item import SaleItemRequest, SaleItemResponse


class CheckoutRequest(BaseModel):
    customer_id: Optional[int] = None
    items: List[SaleItemRequest] = Field(..., min_length=1)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    payment: PaymentRequest


class SaleResponse(BaseModel):
    sale_id: int
    invoice_number: str
    customer_id: Optional[int]
    user_id: int
    subtotal: Decimal
    discount_amount: Decimal
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)


class CheckoutResponse(BaseModel):
    sale: SaleResponse
    items: List[SaleItemResponse]
    payment: PaymentResponse
    receipt: ReceiptResponse