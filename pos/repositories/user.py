from typing import Optional, Sequence

from sqlalchemy.orm import Session

from pos.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = User

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(self.model, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(self.model).filter(self.model.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 50) -> Sequence[User]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: dict) -> User:
        db_user = self.model(**data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, data: dict) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False