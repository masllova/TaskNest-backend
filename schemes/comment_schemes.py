from typing import Dict, Any
from pydantic import BaseModel
from schemes.person_scheme import Person
from datetime import datetime

class UpdateComment(BaseModel):
    creation_date: datetime = datetime.now()
    description: str
    is_updated: bool = False

class GetComment(UpdateComment):
    id: int
    author: Person

    def __init__(self, id: int, comment: UpdateComment, author: Person):
        super().__init__(
            id=id,
            author=author,
            creation_date=comment.creation_date,
            description=comment.description,
            is_updated=comment.is_updated
        )

    def update(self, desc: str):
        self.is_updated=True
        self.creation_date=datetime.now()
        self.description=desc
        return self

    def to_dict(self) -> dict:
        data = self.dict()
        data['creation_date'] = self.creation_date.isoformat()
        return data

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return GetComment(
            id=dict.get('id'),
            comment=UpdateComment(
                creation_date=dict.get('creation_date'),
                description=dict.get('description'),
                is_updated=dict.get('is_updated')
                ),
                author=Person.from_dict(dict.get('author'))
        )



