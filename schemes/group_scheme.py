from pydantic import BaseModel
from typing import List
from schemes.person_scheme import Person

class GetGroup(BaseModel):
    id: int
    name: str
    admin_id: int
    users: List[Person]
    management_access: bool

    def __init__(self, id: int, name: str, admin_id: int, users: List[Person], id_to_exclude: int):
        super().__init__(
            id=id,
            name=name, 
            admin_id=admin_id,
            users=[user for user in users if user.id != id_to_exclude],
            management_access=admin_id==id_to_exclude
            )
        
class GroupCodeResponse(BaseModel):
    code: str
    life_time: int
