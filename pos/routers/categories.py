from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import get_current_user, require_manager
from pos.models.user import User
from pos.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from pos.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    current_user: User = Depends(require_manager),
    service: CategoryService = Depends(get_service),
):
    return service.create(payload)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_service),
):
    return service.get_by_id(category_id)


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_service),
):
    return service.list_all(skip, limit)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    current_user: User = Depends(require_manager),
    service: CategoryService = Depends(get_service),
):
    return service.update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: User = Depends(require_manager),
    service: CategoryService = Depends(get_service),
):
    service.delete(category_id)
    return None