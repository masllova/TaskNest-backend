from typing import Optional
from pydantic import BaseModel, Field

class UpdateComment(BaseModel):
    creation_date: str
    description: str
    is_updated: bool = False

class AddComment(UpdateComment):
    author: str

class CommentAddResponse(BaseModel):
    ok: bool = True
    comment_id: int

class GetComment(AddComment):
    id: int

