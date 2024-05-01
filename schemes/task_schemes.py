from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from schemes.comment_schemes import GetComment
from schemes.person_scheme import Person

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
    dict_id: int

class GetTask(AddTask):
    id: int
    comments: List[GetComment]
    author: Optional[Person] = None

    def __init__(self, id: int, task: AddTask, author: Person, comments: [GetComment]):
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

    def add_comment(self, data: GetComment):
        self.comments.append(data)
        return self

    def update_comment(self, data: GetComment):
        for comment in self.comments:
            if comment.id == data.id:
                comment.creation_date = data.creation_date
                comment.description = data.description
                comment.is_updated = data.is_updated
                return self
        return None


    def to_dict(self) -> dict:
        data = self.dict()
        data['creation_date'] = self.creation_date.isoformat()
        if self.deadline:
            data['deadline'] = self.deadline.isoformat()
        else:
            data['deadline'] = None

        if self.comments:
            data['comments'] = [comment_dict.to_dict() for comment_dict in self.comments]
        else:
            data['comments'] = []

        if self.author:
            data['author'] = self.author.dict()
        else:
            data['author'] = None
        return data

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return GetTask(
            id=dict.get('id'),
            task=AddTask(
                name=dict.get('name'),
                is_completed=dict.get('is_completed'),
                color_hex=dict.get('color_hex'),
                creation_date=dict.get('creation_date'),
                deadline=dict.get('deadline'),
                description=dict.get('description')
            ),
            author=Person.from_dict(dict.get('author')),
            comments=[GetComment.from_dict(comment_dict) for comment_dict in dict.get('comments', [])]
        )

