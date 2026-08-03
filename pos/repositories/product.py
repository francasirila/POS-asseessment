from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.get(self.model, product_id)

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        return self.db.query(self.model).filter(self.model.barcode == barcode).first()

    def get_all(
        self, skip: int = 0, limit: int = 50, category_id: Optional[int] = None
    ) -> Sequence[Product]:
        query = self.db.query(self.model)
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
        return query.offset(skip).limit(limit).all()

    def create(self, data: dict) -> Product:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def update(self, product_id: int, data: dict) -> Optional[Product]:
        db_record = self.get_by_id(product_id)
        if db_record:
            for key, value in data.items():
                setattr(db_record, key, value)
            self.db.commit()
            self.db.refresh(db_record)
        return db_record

    def decrement_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        db_record = self.get_by_id(product_id)
        if db_record:
            db_record.stock_quantity -= quantity
            self.db.flush()
        return db_record

    def delete(self, product_id: int) -> bool:
        db_record = self.get_by_id(product_id)
        if db_record:
            self.db.delete(db_record)
            self.db.commit()
            return True
        return False