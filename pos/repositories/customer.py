from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db.get(self.model, customer_id)

    def get_by_phone(self, phone_number: str) -> Optional[Customer]:
        return self.db.query(self.model).filter(self.model.phone_number == phone_number).first()

    def get_all(self, skip: int = 0, limit: int = 50) -> Sequence[Customer]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: dict) -> Customer:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def update(self, customer_id: int, data: dict) -> Optional[Customer]:
        db_record = self.get_by_id(customer_id)
        if db_record:
            for key, value in data.items():
                setattr(db_record, key, value)
            self.db.commit()
            self.db.refresh(db_record)
        return db_record

    def delete(self, customer_id: int) -> bool:
        db_record = self.get_by_id(customer_id)
        if db_record:
            self.db.delete(db_record)
            self.db.commit()
            return True
        return False