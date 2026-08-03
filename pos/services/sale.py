import secrets
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.payment import PaymentStatus
from pos.models.sale import Sale
from pos.repositories.customer import CustomerRepository
from pos.repositories.payment import PaymentRepository
from pos.repositories.product import ProductRepository
from pos.repositories.receipt import ReceiptRepository
from pos.repositories.sale import SaleRepository
from pos.repositories.sale_item import SaleItemRepository
from pos.schemas.sale import CheckoutRequest


def _money(value) -> Decimal:
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_repo = SaleRepository(db)
        self.item_repo = SaleItemRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.receipt_repo = ReceiptRepository(db)
        self.product_repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)

    def checkout(self, user_id: int, request: CheckoutRequest):
        if request.customer_id is not None and not self.customer_repo.get_by_id(request.customer_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        try:
            resolved_items = []
            subtotal = Decimal("0.00")

            for item in request.items:
                product = self.product_repo.get_by_id(item.product_id)
                if not product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {item.product_id} not found",
                    )
                if product.stock_quantity < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Insufficient stock for '{product.name}'",
                    )
                unit_price = _money(item.unit_price) if item.unit_price is not None else _money(product.selling_price)
                subtotal += unit_price * item.quantity
                resolved_items.append((product, item.quantity, unit_price))

            subtotal = _money(subtotal)
            discount_amount = _money(request.discount_amount)
            if discount_amount > subtotal:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Discount cannot exceed subtotal",
                )
            total_amount = _money(subtotal - discount_amount)

            amount_paid = _money(request.payment.amount_paid)
            if amount_paid < total_amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Amount paid is less than the total due",
                )

            invoice_number = f"INV-{datetime.now(timezone.utc):%Y%m%d}-{secrets.token_hex(3).upper()}"
            sale = self.sale_repo.create(
                {
                    "invoice_number": invoice_number,
                    "customer_id": request.customer_id,
                    "user_id": user_id,
                    "subtotal": subtotal,
                    "discount_amount": discount_amount,
                    "total_amount": total_amount,
                }
            )

            created_items = []
            for product, quantity, unit_price in resolved_items:
                created_items.append(
                    self.item_repo.create(
                        {
                            "sale_id": sale.sale_id,
                            "product_id": product.product_id,
                            "quantity": quantity,
                            "unit_price": unit_price,
                        }
                    )
                )
                self.product_repo.decrement_stock(product.product_id, quantity)

            payment = self.payment_repo.create(
                {
                    "sale_id": sale.sale_id,
                    "method": request.payment.method,
                    "amount_paid": amount_paid,
                    "status": PaymentStatus.completed,
                    "transaction_reference": request.payment.transaction_reference,
                }
            )

            receipt_number = f"RCPT-{datetime.now(timezone.utc):%Y%m%d}-{secrets.token_hex(3).upper()}"
            receipt = self.receipt_repo.create(
                {
                    "sale_id": sale.sale_id,
                    "receipt_number": receipt_number,
                    "issued_at": datetime.now(timezone.utc),
                    "total_amount": total_amount,
                }
            )

            self.db.commit()
            self.db.refresh(sale)
            for item in created_items:
                self.db.refresh(item)
            self.db.refresh(payment)
            self.db.refresh(receipt)

            return sale, created_items, payment, receipt

        except HTTPException:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Checkout failed"
            )

    def get_sale(self, sale_id: int) -> Sale:
        sale = self.sale_repo.get_by_id(sale_id)
        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
        return sale

    def list_sales(self, skip: int = 0, limit: int = 50, user_id=None) -> Sequence[Sale]:
        return self.sale_repo.get_all(skip, limit, user_id)

    def get_items(self, sale_id: int):
        self.get_sale(sale_id)
        return self.item_repo.get_by_sale(sale_id)

    def get_payment(self, sale_id: int):
        self.get_sale(sale_id)
        payment = self.payment_repo.get_by_sale(sale_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        return payment

    def get_receipt(self, sale_id: int):
        self.get_sale(sale_id)
        receipt = self.receipt_repo.get_by_sale(sale_id)
        if not receipt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
        return receipt

    def update_payment_status(self, payment_id: int, new_status: PaymentStatus):
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        return self.payment_repo.update_status(payment_id, new_status)