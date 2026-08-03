from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ReceiptResponse(BaseModel):
    receipt_id: int
    sale_id: int
    receipt_number: str
    issued_at: datetime
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)