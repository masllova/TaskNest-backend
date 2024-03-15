from fastapi import APIRouter, Depends
from typing import Annotated
from shemas.task_scemas import AddTask, GetTask, TaskAddResponse
from methods.task.task_repository import TaskRepository

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

@router.get('')
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.get_all()
    return tasks

@router.post('')
async def add_tasks(
    task: Annotated[AddTask, Depends()]
) -> TaskAddResponse:
    task_id = await TaskRepository.add_one(task)
    return TaskAddResponse(task_id=task_id)

@router.delete('/{task_id}')
async def delete_task(task_id: int) -> bool:
    success = await TaskRepository.delete_by_id(task_id)
    return success

@router.put('/{task_id}')
async def update_task(task_id: int, task: Annotated[AddTask, Depends()]) -> bool:
    success = await TaskRepository.update_by_id(task_id, task)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return success