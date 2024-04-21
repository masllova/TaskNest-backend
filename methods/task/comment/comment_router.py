from fastapi import APIRouter, Header
from schemes.comment_schemes import GetComment, UpdateComment
from methods.task.comment.comment_repository import CommentRepository

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)

@router.post('')
async def add_comment(
    user_id: int,
    task_id: int,
    description: str,
    token: str = Header(None)
) -> bool:
    success = await CommentRepository.add_one(token, task_id, description, user_id)
    return success

@router.delete('/{task_id}/comment/{comment_id}')
async def delete_comment(
    user_id: int,
    task_id: int,
    comment_id: int,
    token: str = Header(None)
) -> bool:
    success = await CommentRepository.delete_by_id(token, user_id, task_id, comment_id)
    return success

@router.put('{user_id}/task/{task_id}/comment/{comment_id}')
async def update_comment(
    user_id: int,
    task_id: int,
    comment_id: int,
    description: str,
    token: str = Header(None)
) -> bool:
    success = await CommentRepository.update_by_id(token, user_id, task_id, comment_id, description)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return success