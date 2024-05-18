from fastapi import APIRouter, Depends, Header
from typing import Annotated, Optional
from schemes.task_schemes import AddTask, GetTask, UpdateTask, TaskAddResponse
from methods.task.task_repository import TaskRepository

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

@router.get('/')
async def get_tasks(
    token: str = Header(None),
    user_id: Optional[int] = None
) -> list[GetTask]:
    tasks = await TaskRepository.get_all(token, user_id)
    return tasks

@router.post('/')
async def add_tasks(
    task: Annotated[AddTask, Depends()],
    token: str = Header(None),
    user_id: Optional[int] = None
) -> bool:
    success = await TaskRepository.add_one(token, task, user_id)
    return success

@router.delete('/{task_id}/')
async def delete_task(
    task_id: int,
    token: str = Header(None)
) -> bool:
    success = await TaskRepository.delete_by_id(token, task_id)
    return success

@router.put('/{task_id}/')
async def update_task(
    task_id: int, 
    task: Annotated[UpdateTask, Depends()],
    token: str = Header(None)
) -> bool:
    success = await TaskRepository.update_by_id(token, task_id, task)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return success