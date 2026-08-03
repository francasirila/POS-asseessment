from typing import Optional

from sqlalchemy.orm import Session

from pos.models.receipt import Receipt


class ReceiptRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Receipt

    def get_by_id(self, receipt_id: int) -> Optional[Receipt]:
        return self.db.get(self.model, receipt_id)

    def get_by_sale(self, sale_id: int) -> Optional[Receipt]:
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def create(self, data: dict) -> Receipt:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.flush()
        return db_record