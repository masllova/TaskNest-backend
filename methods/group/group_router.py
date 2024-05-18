from fastapi import APIRouter, Depends, Header
from typing import Annotated, Optional
from schemes.group_scheme import GetGroup, GroupCodeResponse
from methods.group.group_repository import GroupRepository

router = APIRouter(
    prefix='/group',
    tags=['Group']
)

@router.post('/')
async def create_new_group(
    name: str, 
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.create_new_group(token=token, name=name)
    return group

@router.get('/')
async def get_user_group_info(
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.get_user_group_info(token=token)
    return group

@router.delete('/')
async def delete_group( 
    token: str = Header(None)
) -> bool:
    success = await GroupRepository.delete_group(token=token)
    return success

@router.get('/join_code/')
async def generate_join_code(
    token: str = Header(None)
) -> Optional[GroupCodeResponse]:
    code = await GroupRepository.generate_join_code(token=token)
    return code

@router.put('/join_code/')
async def join_group(
    code: int, 
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.join_group(token=token, join_code=code)
    return group

@router.put('/admin/')
async def change_admin(
    new_admin_id: int,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.change_admin(token=token, new_admin_id=new_admin_id)
    return group

@router.put('/name/')
async def change_group_name(
    new_name: str,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.change_group_name(token=token, new_name=new_name)
    return group

@router.delete('/user/')
async def remove_user_from_group(
    user_id: int,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.remove_user_from_group(token=token, user_id=user_id)
    return group