from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.supplier import Supplier


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Supplier

    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.db.get(self.model, supplier_id)

    def get_all(self, skip: int = 0, limit: int = 50) -> Sequence[Supplier]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: dict) -> Supplier:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def update(self, supplier_id: int, data: dict) -> Optional[Supplier]:
        db_record = self.get_by_id(supplier_id)
        if db_record:
            for key, value in data.items():
                setattr(db_record, key, value)
            self.db.commit()
            self.db.refresh(db_record)
        return db_record

    def delete(self, supplier_id: int) -> bool:
        db_record = self.get_by_id(supplier_id)
        if db_record:
            self.db.delete(db_record)
            self.db.commit()
            return True
        return False