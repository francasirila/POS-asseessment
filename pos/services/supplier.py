from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.supplier import Supplier
from pos.repositories.supplier import SupplierRepository
from pos.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    def __init__(self, db: Session):
        self.repo = SupplierRepository(db)

    def create(self, schema: SupplierCreate) -> Supplier:
        return self.repo.create(schema.model_dump())

    def get_by_id(self, supplier_id: int) -> Supplier:
        record = self.repo.get_by_id(supplier_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return record

    def list_all(self, skip: int = 0, limit: int = 50) -> Sequence[Supplier]:
        return self.repo.get_all(skip, limit)

    def update(self, supplier_id: int, schema: SupplierUpdate) -> Supplier:
        self.get_by_id(supplier_id)
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(supplier_id, update_data)

    def delete(self, supplier_id: int) -> None:
        self.get_by_id(supplier_id)
        self.repo.delete(supplier_id)