from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import assert_own_sale_or_manager, get_current_user, require_manager
from pos.models.user import User
from pos.schemas.payment import PaymentResponse, PaymentStatusUpdate
from pos.schemas.receipt import ReceiptResponse
from pos.schemas.sale import CheckoutRequest, CheckoutResponse, SaleResponse
from pos.schemas.sale_item import SaleItemResponse
from pos.services.sale import SaleService

router = APIRouter(prefix="/sales", tags=["Sales"])


def get_service(db: Session = Depends(get_db)) -> SaleService:
    return SaleService(db)


@router.post("/checkout", response_model=CheckoutResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    payload: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    sale, items, payment, receipt = service.checkout(current_user.user_id, payload)
    return CheckoutResponse(sale=sale, items=items, payment=payment, receipt=receipt)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    sale = service.get_sale(sale_id)
    assert_own_sale_or_manager(sale.user_id, current_user)
    return sale


@router.get("", response_model=List[SaleResponse])
def list_sales(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    user_filter = None if current_user.role == "manager" else current_user.user_id
    return service.list_sales(skip, limit, user_filter)


@router.get("/{sale_id}/items", response_model=List[SaleItemResponse])
def get_sale_items(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    sale = service.get_sale(sale_id)
    assert_own_sale_or_manager(sale.user_id, current_user)
    return service.get_items(sale_id)


@router.get("/{sale_id}/payment", response_model=PaymentResponse)
def get_sale_payment(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    sale = service.get_sale(sale_id)
    assert_own_sale_or_manager(sale.user_id, current_user)
    return service.get_payment(sale_id)


@router.get("/{sale_id}/receipt", response_model=ReceiptResponse)
def get_sale_receipt(
    sale_id: int,
    current_user: User = Depends(get_current_user),
    service: SaleService = Depends(get_service),
):
    sale = service.get_sale(sale_id)
    assert_own_sale_or_manager(sale.user_id, current_user)
    return service.get_receipt(sale_id)


@router.patch("/payments/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(
    payment_id: int,
    payload: PaymentStatusUpdate,
    current_user: User = Depends(require_manager),
    service: SaleService = Depends(get_service),
):
    return service.update_payment_status(payment_id, payload.status)