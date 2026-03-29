from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schema import UserRegister, UserLogin

class UserService:
    @staticmethod
    def register_user(db: Session, user_in: UserRegister):
        if UserRepository.get_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
            )
        
        hashed_pw = hash_password(user_in.password)
        return UserRepository.create(db, user_in.email, hashed_pw)

    @staticmethod
    def authenticate_user(db: Session, user_in: UserLogin):
        user = UserRepository.get_by_email(db, user_in.email)
        if not user or not verify_password(user_in.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}