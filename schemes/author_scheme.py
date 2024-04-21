from pydantic import BaseModel
from typing import Optional, Dict, Any

class Author(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_dict(dict: Optional[Dict[str, Any]]):
        if dict:
            return Author(
                id=dict.get('id'),
                name=dict.get('name')
            )
        else: 
            return None

