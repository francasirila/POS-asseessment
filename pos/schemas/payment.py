from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from pos.models.payment import PaymentMethod, PaymentStatus


class PaymentRequest(BaseModel):
    method: PaymentMethod
    amount_paid: Decimal = Field(..., ge=0, decimal_places=2)
    transaction_reference: Optional[str] = Field(None, max_length=100)


class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus


class PaymentResponse(BaseModel):
    payment_id: int
    sale_id: int
    method: PaymentMethod
    amount_paid: Decimal
    status: PaymentStatus
    transaction_reference: Optional[str]

    model_config = ConfigDict(from_attributes=True)