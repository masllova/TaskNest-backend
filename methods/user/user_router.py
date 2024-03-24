from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from shemas.user_scemas import UserCreate, AuthResponse, UserBase, GetUser
from methods.user.user_repository import UserRepository

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/registrationtion')
async def create_new_user(
    data: Annotated[UserCreate, Depends()]
) -> AuthResponse:
    return await UserRepository.create_new_user(data)

@router.get('/authorization')
async def check_user_authorization(
    data: Annotated[UserCreate, Depends()]
    ) -> Optional[AuthResponse]:
    return await UserRepository.check_user_authorization(data)

@router.get('/{user_id}')
async def get_user_info(user_id: int) -> Optional[GetUser]:
    user = await UserRepository.get_user_info(user_id)
    return user

@router.put('/{user_id}')
async def update_user_info_by_id(user_id: int, info: Annotated[UserBase, Depends()]) -> bool:
    success = await UserRepository.update_user_info_by_id(user_id, info)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success
