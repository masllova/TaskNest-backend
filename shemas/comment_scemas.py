from typing import Optional
from pydantic import BaseModel, Field

class UpdateComment(BaseModel):
    creation_date: str
    description: str
    is_updated: bool = True

class AddComment(UpdateComment):
    author: str
    author_emoji: str

class CommentAddResponse(BaseModel):
    ok: bool = True
    comment_id: int

class GetComment(AddComment):
    id: int

