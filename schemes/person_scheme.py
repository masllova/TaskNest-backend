from pydantic import BaseModel
from typing import Optional, Dict, Any

class Person(BaseModel):
    id: int
    name: str
    emoji: str

    @staticmethod
    def from_dict(dict: Optional[Dict[str, Any]]):
        if dict:
            return Person(
                id=dict.get('id'),
                name=dict.get('name'),
                emoji=dict.get('emoji')
            )
        else: 
            return None

