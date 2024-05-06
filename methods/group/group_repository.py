from typing import Optional
from sqlalchemy import select
from db.group_database import Group, new_session
from managers.jwt_manager import JWTManager
from managers.user_data_manager import UserDataManager
from schemes.group_scheme import *
import jwt

class GroupRepository:
    @classmethod
    async def create_new_group(cls, token: str, name: str) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    async with session.begin():
                        author = await UserDataManager.get_person_by_id(decoded_user_id)
                        new_group = Group(
                            name=name, 
                            admin_id=decoded_user_id, 
                            users=[author.to_dict()]
                            )
                        session.add(new_group)
                        await session.flush()
                        await session.commit()
                    await session.refresh(new_group)
                    return True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return False

    @classmethod
    async def get_group_by_id(cls, token: str, group_id: int) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    group = await session.execute(select(Group).filter(Group.id == group_id))
                    group_data = group.scalars().first()
                    if group_data:
                        users_data = [Person.from_dict(user) for user in group_data.users]
                        return GetGroup(
                            id=group_data.id,
                            name=group_data.name,
                            admin_id=group_data.admin_id,
                            users=users_data
                        )

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None