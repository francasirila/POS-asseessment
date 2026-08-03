from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.models.customer import Customer
from pos.repositories.customer import CustomerRepository
from pos.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def create(self, schema: CustomerCreate) -> Customer:
        if self.repo.get_by_phone(schema.phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Phone number already registered"
            )
        return self.repo.create(schema.model_dump())

    def get_by_id(self, customer_id: int) -> Customer:
        record = self.repo.get_by_id(customer_id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return record

    def list_all(self, skip: int = 0, limit: int = 50) -> Sequence[Customer]:
        return self.repo.get_all(skip, limit)

    def update(self, customer_id: int, schema: CustomerUpdate) -> Customer:
        self.get_by_id(customer_id)
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(customer_id, update_data)

    def delete(self, customer_id: int) -> None:
        self.get_by_id(customer_id)
        self.repo.delete(customer_id)