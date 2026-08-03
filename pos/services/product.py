from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.product import Product
from pos.repositories.category import CategoryRepository
from pos.repositories.product import ProductRepository
from pos.repositories.supplier import SupplierRepository
from pos.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.supplier_repo = SupplierRepository(db)

    def create(self, schema: ProductCreate) -> Product:
        if not self.category_repo.get_by_id(schema.category_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if schema.supplier_id is not None and not self.supplier_repo.get_by_id(schema.supplier_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        if schema.barcode and self.repo.get_by_barcode(schema.barcode):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Barcode already registered"
            )
        return self.repo.create(schema.model_dump())

    def get_by_id(self, product_id: int) -> Product:
        record = self.repo.get_by_id(product_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return record

    def get_by_barcode(self, barcode: str) -> Product:
        record = self.repo.get_by_barcode(barcode)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return record

    def list_all(
        self, skip: int = 0, limit: int = 50, category_id: Optional[int] = None
    ) -> Sequence[Product]:
        return self.repo.get_all(skip, limit, category_id)

    def update(self, product_id: int, schema: ProductUpdate) -> Product:
        self.get_by_id(product_id)
        update_data = schema.model_dump(exclude_unset=True)
        if "category_id" in update_data and not self.category_repo.get_by_id(update_data["category_id"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        if "supplier_id" in update_data and update_data["supplier_id"] is not None:
            if not self.supplier_repo.get_by_id(update_data["supplier_id"]):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return self.repo.update(product_id, update_data)

    def delete(self, product_id: int) -> None:
        self.get_by_id(product_id)
        self.repo.delete(product_id)