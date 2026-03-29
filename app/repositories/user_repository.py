from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        stmt = select(User).filter(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        stmt = select(User).filter(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def create(db: Session, email: str, hashed_pw: str):
        db_user = User(email=email, password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user