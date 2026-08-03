from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from pos.core.security import create_access_token, hash_password, verify_password
from pos.models.user import User
from pos.repositories.user import UserRepository
from pos.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_staff(self, schema: UserCreate) -> User:
        if self.repo.get_by_email(schema.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )
        if schema.username and self.repo.get_by_username(schema.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
            )

        data = schema.model_dump(exclude={"password"})
        data["password_hash"] = hash_password(schema.password)
        return self.repo.create(data)

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not user.is_active or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
            )
        return create_access_token(user.user_id, user.role.value)

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 50):
        return self.repo.get_all(skip, limit)

    def update_user(self, user_id: int, schema: UserUpdate) -> User:
        self.get_user(user_id)
        update_data = schema.model_dump(exclude_unset=True)
        return self.repo.update(user_id, update_data)

    def delete_user(self, user_id: int) -> None:
        self.get_user(user_id)
        self.repo.delete(user_id)