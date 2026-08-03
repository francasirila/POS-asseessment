from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.get(self.model, category_id)

    def get_all(self, skip: int = 0, limit: int = 50) -> Sequence[Category]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: dict) -> Category:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def update(self, category_id: int, data: dict) -> Optional[Category]:
        db_record = self.get_by_id(category_id)
        if db_record:
            for key, value in data.items():
                setattr(db_record, key, value)
            self.db.commit()
            self.db.refresh(db_record)
        return db_record

    def delete(self, category_id: int) -> bool:
        db_record = self.get_by_id(category_id)
        if db_record:
            self.db.delete(db_record)
            self.db.commit()
            return True
        return False