from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class AddTask(BaseModel):
    name: str
    is_completed: bool
    color_hex: str
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

