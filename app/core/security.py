from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

def hash_password(password: str) -> str:
    # No hashing - just returns the plain string
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Direct string comparison
    return plain_password == hashed_password

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)