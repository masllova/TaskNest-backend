from fastapi import APIRouter, Depends, Header
from typing import Annotated, Optional
from schemes.group_scheme import GetGroup
from methods.group.group_repository import GroupRepository

router = APIRouter(
    prefix='/group',
    tags=['Group']
)

@router.post('/')
async def create_new_group(
    name: str, 
    token: str = Header(None)
) -> bool:
    success = await GroupRepository.create_new_group(token=token, name=name)
    return success

@router.get('/')
async def get_group_by_id(
    id: int, 
    token: str = Header(None)
) -> Optional[GetGroup]:
    group = await GroupRepository.get_group_by_id(token=token, group_id=id)
    return group