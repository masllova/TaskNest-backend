from typing import Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum

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

class AuthResponse(BaseModel):
    message: str
    jwt: Optional[str] = None
    user: Optional[GetUser] = None

class AuthStatus(Enum):
    NOT_FOUND = 'not_found'
    INCORRECT_PASSWORD = 'incorrect_password'
    WELCOME = 'welcome'
    SUCCESSFUL = 'successful'
