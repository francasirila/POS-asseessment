from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import get_current_user, require_manager
from pos.models.user import User
from pos.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from pos.services.customer import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_service),
):
    return service.create(payload)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_service),
):
    return service.get_by_id(customer_id)


@router.get("", response_model=List[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_service),
):
    return service.list_all(skip, limit)


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    service: CustomerService = Depends(get_service),
):
    return service.update(customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    current_user: User = Depends(require_manager),
    service: CustomerService = Depends(get_service),
):
    service.delete(customer_id)
    return None