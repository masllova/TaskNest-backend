from fastapi import APIRouter, Depends, Header
from typing import Annotated, Optional
from schemes.user_schemes import UserCreate, AuthResponse, UserBase, GetUser
from methods.user.user_repository import UserRepository

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/registrationtion/')
async def create_new_user(
    data: Annotated[UserCreate, Depends()]
) -> AuthResponse:
    return await UserRepository.create_new_user(data)

@router.get('/authorization/')
async def check_user_authorization(
    data: Annotated[UserCreate, Depends()]
) -> Optional[AuthResponse]:
    return await UserRepository.check_user_authorization(data)

@router.get('/')
async def get_user_info(
    token: str = Header(None), 
    user_id: Optional[int] = None
) -> Optional[GetUser]:
    user = await UserRepository.get_user_info(token, user_id)
    return user

@router.put('/')
async def update_user_info(
    info: Annotated[UserBase, Depends()], 
    token: str = Header(None)
) -> Optional[GetUser]:
    success = await UserRepository.update_user_info(token, info)
    return success
