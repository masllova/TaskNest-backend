from typing import Optional
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = '👤'
    birthday: Optional[date] = None
    status: Optional[str] = None

class UserCreate(BaseModel):
    mail: str
    password: str

class GetUser(UserBase):
    id: int

    class Config:
        orm_mode = True

class AuthResponse(BaseModel):
    isVerified: bool
    user: Optional[GetUser]
