from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from shemas.comment_scemas import GetComment

class UpdateTask(BaseModel):
    name: Optional[str] = None
    is_completed: bool
    color_hex: Optional[str] = None
    deadline: Optional[datetime] = None
    description: Optional[str] = None

class AddTask(UpdateTask):
    name: str
    creation_date: datetime = datetime.now()

class TaskAddResponse(BaseModel):
    ok: bool = True
    task_id: int

class Author(BaseModel):
    id: int
    name: Optional[str]

class GetTask(AddTask):
    id: int
    comments: List[GetComment]
    author: Author

    def __init__(self, id: int, task: AddTask, author: Author, comments: [GetComment]):
        super().__init__(
            name=task.name,
            is_completed=task.is_completed,
            color_hex=task.color_hex,
            creation_date=task.creation_date,
            deadline=task.deadline,
            description=task.description,
            comments=comments,
            author=author,
            id=id
        )

    def update(self, data: UpdateTask):
        self.is_completed = data.is_completed

        if data.name:
            self.name = data.name
        if data.color_hex:
            self.color_hex = data.color_hex
        if data.deadline:
            self.deadline = data.deadline
        if data.description:
            self.description = data.description
        return self

    def to_dict(self) -> dict:
        data = self.dict()
        data['creation_date'] = self.creation_date.isoformat()
        if self.deadline:
            data['deadline'] = self.deadline.isoformat()
        else:
            data['deadline'] = None

        if self.comments:
            data['comments'] = [comment.dict() for comment in self.comments]
        else:
            data['comments'] = []

        data['author'] = self.author.dict()
        return data

    @staticmethod
    def from_dict(task: Dict[str, Any]):
        return GetTask(
            id=task.get('id'),
            task=AddTask(
                name=task.get('name'),
                is_completed=task.get('is_completed'),
                color_hex=task.get('color_hex'),
                creation_date=task.get('creation_date'),
                deadline=task.get('deadline'),
                description=task.get('description')
            ),
            author=Author(
                id=task['author'].get('id'),
                name=task['author'].get('name')
            ),
            comments=[
                GetComment(
                    id=comment.get('id'),
                    creation_date=comment.get('creation_date'),
                    description=comment.get('description'),
                    is_updated=comment.get('is_updated'),
                    author=comment.get('author'),
                ) for comment in task.get('comments', [])
                ]
        )
