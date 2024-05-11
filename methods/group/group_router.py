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