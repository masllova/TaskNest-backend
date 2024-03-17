from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from shemas.comment_scemas import GetComment

class AddTask(BaseModel):
    name: str
    is_completed: bool
    color_hex: Optional[str] = None
    author: str
    author_emoji: str
    creation_date: datetime
    deadline: Optional[datetime] = None
    description: Optional[str] = None

class TaskAddResponse(BaseModel):
    ok: bool = True
    task_id: int

class GetTask(AddTask):
    id: int
    comments: Optional[List[GetComment]] = None