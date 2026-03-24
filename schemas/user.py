# schemas/user.py
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True




