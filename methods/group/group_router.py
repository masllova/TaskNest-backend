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
async def get_group_by_id(
    id: int, 
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.get_group_by_id(token=token, group_id=id)
    return group

@router.delete('/')
async def delete_group(
    id: int, 
    token: str = Header(None)
) -> bool:
    success = await GroupRepository.delete_group(token=token, group_id=id)
    return success

@router.get('/join_code')
async def generate_join_code(
    id: int
) -> GroupCodeResponse:
    code = await GroupRepository.generate_join_code(group_id=id)
    return code

@router.put('/join_code')
async def join_group(
    code: int, 
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.join_group(token=token, join_code=code)
    return group

@router.put('/admin')
async def change_admin(
    group_id: int, 
    new_admin_id: int,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.change_admin(token=token, group_id=group_id, new_admin_id=new_admin_id)
    return group

@router.put('/name')
async def change_group_name(
    group_id: int, 
    new_name: str,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.change_group_name(token=token, group_id=group_id, new_name=new_name)
    return group

@router.delete('/user')
async def remove_user_from_group(
    group_id: int, 
    user_id: int,
    token: str  = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.remove_user_from_group(token=token, group_id=group_id, user_id=user_id)
    return group