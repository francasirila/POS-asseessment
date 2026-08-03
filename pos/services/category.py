from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.category import Category
from pos.repositories.category import CategoryRepository
from pos.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create(self, schema: CategoryCreate) -> Category:
        return self.repo.create(schema.model_dump())

    def get_by_id(self, category_id: int) -> Category:
        record = self.repo.get_by_id(category_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return record

    def list_all(self, skip: int = 0, limit: int = 50) -> Sequence[Category]:
        return self.repo.get_all(skip, limit)

    def update(self, category_id: int, schema: CategoryUpdate) -> Category:
        self.get_by_id(category_id)
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(category_id, update_data)

    def delete(self, category_id: int) -> None:
        self.get_by_id(category_id)
        self.repo.delete(category_id)