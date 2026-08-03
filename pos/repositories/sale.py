from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.sale import Sale


class SaleRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Sale

    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        return self.db.get(self.model, sale_id)

    def get_all(
        self, skip: int = 0, limit: int = 50, user_id: Optional[int] = None
    ) -> Sequence[Sale]:
        query = self.db.query(self.model)
        if user_id is not None:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.sale_id.desc()).offset(skip).limit(limit).all()

    def create(self, data: dict) -> Sale:
        db_record = self.model(**data)
        self.db.add(db_record)
        self.db.flush()
        return db_record