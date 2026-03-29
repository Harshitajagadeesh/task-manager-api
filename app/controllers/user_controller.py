from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.user_service import UserService
from app.schemas.response_schema import APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    UserService.register_user(db, user_in)
    return {
        "success": True, 
        "message": "User registered successfully", 
        "data": None
    }

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    token_data = UserService.authenticate_user(db, user_in)
    return {
        "success": True,
        "message": "Login successful",
        "data": token_data
    }