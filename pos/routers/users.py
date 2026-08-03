from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from pos.core.security import get_current_user, require_manager
from pos.models.user import User
from pos.schemas.user import UserCreate, UserResponse, UserUpdate
from pos.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: UserCreate,
    current_user: User = Depends(require_manager),
    service: UserService = Depends(get_service),
):
    return service.create_staff(payload)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_manager),
    service: UserService = Depends(get_service),
):
    return service.list_users(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(require_manager),
    service: UserService = Depends(get_service),
):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    current_user: User = Depends(require_manager),
    service: UserService = Depends(get_service),
):
    return service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_manager),
    service: UserService = Depends(get_service),
):
    service.delete_user(user_id)
    return None