from pydantic import BaseModel
from typing import List
from schemes.person_scheme import Person

class GetGroup(BaseModel):
    id: int
    name: str
    admin_id: int
    users: List[Person]

