from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr

class UserRegister(UserBase):
    # We set max_length to 72 to align with the Bcrypt standard
    password: str = Field(..., min_length=6, max_length=72)

class UserLogin(UserBase):
    password: str = Field(..., max_length=72)

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)