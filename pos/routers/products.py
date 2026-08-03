from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import get_current_user, require_manager
from pos.models.user import User
from pos.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from pos.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    current_user: User = Depends(require_manager),
    service: ProductService = Depends(get_service),
):
    return service.create(payload)


@router.get("/barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(
    barcode: str,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_service),
):
    return service.get_by_barcode(barcode)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_service),
):
    return service.get_by_id(product_id)


@router.get("", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 50,
    category_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_service),
):
    return service.list_all(skip, limit, category_id)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    current_user: User = Depends(require_manager),
    service: ProductService = Depends(get_service),
):
    return service.update(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(require_manager),
    service: ProductService = Depends(get_service),
):
    service.delete(product_id)
    return None