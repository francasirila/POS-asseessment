from typing import Sequence

from sqlalchemy.orm import Session

from pos.models.sale_item import SaleItem


class SaleItemRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = SaleItem

    def get_by_sale(self, sale_id: int) -> Sequence[SaleItem]:
        return self.db.query(self.model).filter(self.model.sale_id == sale_id).all()

    def create(self, data: dict) -> SaleItem:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.flush()
        return db_record