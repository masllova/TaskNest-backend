from fastapi import APIRouter, Depends
from typing import Annotated
from shemas.comment_scemas import AddComment, GetComment, CommentAddResponse, UpdateComment
from methods.comment.comment_repository import CommentRepository

router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)

@router.post('')
async def add_comment(
    comment: Annotated[AddComment, Depends()],
    task_id: int
) -> CommentAddResponse:
    comment_id = await CommentRepository.add_one(data=comment, task_id=task_id)
    return CommentAddResponse(comment_id=comment_id)

@router.delete('/{task_id}/comment/{comment_id}')
async def delete_comment(task_id: int, comment_id: int) -> bool:
    success = await CommentRepository.delete_by_id(task_id=task_id, comment_id=comment_id)
    return success

@router.put('/{task_id}/comment/{comment_id}')
async def update_comment(task_id: int, comment_id: int, comment: Annotated[UpdateComment, Depends()]) -> bool:
    success = await CommentRepository.update_by_id(task_id=task_id, comment_id=comment_id, data=comment)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return success