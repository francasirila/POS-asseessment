from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import get_current_user, require_manager
from pos.models.user import User
from pos.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from pos.services.supplier import SupplierService

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


def get_service(db: Session = Depends(get_db)) -> SupplierService:
    return SupplierService(db)


@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    payload: SupplierCreate,
    current_user: User = Depends(require_manager),
    service: SupplierService = Depends(get_service),
):
    return service.create(payload)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    current_user: User = Depends(get_current_user),
    service: SupplierService = Depends(get_service),
):
    return service.get_by_id(supplier_id)


@router.get("", response_model=List[SupplierResponse])
def list_suppliers(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    service: SupplierService = Depends(get_service),
):
    return service.list_all(skip, limit)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    current_user: User = Depends(require_manager),
    service: SupplierService = Depends(get_service),
):
    return service.update(supplier_id, payload)


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    current_user: User = Depends(require_manager),
    service: SupplierService = Depends(get_service),
):
    service.delete(supplier_id)
    return None