from typing import Optional

from sqlalchemy.orm import Session

from pos.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Payment

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.db.get(self.model, payment_id)

    def get_by_sale(self, sale_id: int) -> Optional[Payment]:
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def create(self, data: dict) -> Payment:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.flush()
        return db_record

    def update_status(self, payment_id: int, status: str) -> Optional[Payment]:
        db_record = self.get_by_id(payment_id)
        if db_record:
            db_record.status = status
            self.db.commit()
            self.db.refresh(db_record)
        return db_record