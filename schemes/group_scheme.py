from pydantic import BaseModel
from typing import List
from schemes.person_scheme import Person

class GroupCreate(BaseModel):
    name: str
    admin_id: str

class GetGroup(GroupCreate):
    id: int
    users_id: List[Person]

