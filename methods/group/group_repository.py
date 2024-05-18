from typing import Optional
from sqlalchemy import select, update
from db.group_database import Group, new_session
from managers.jwt_manager import JWTManager
from managers.user_data_manager import UserDataManager
from schemes.group_scheme import *
from datetime import datetime
import random
import string
import asyncio
import jwt

class GroupRepository:
    join_codes = {}

    @classmethod
    async def create_new_group(cls, token: str, name: str) -> Optional[GetGroup]:
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
                    return GetGroup(
                        id=new_group.id,
                        name=new_group.name,
                        admin_id=decoded_user_id,
                        users=[],
                        id_to_exclude=decoded_user_id
                    )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None

    @classmethod
    async def get_group_by_id(cls, token: str, group_id: int) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    group = await session.execute(select(Group).filter(Group.id == group_id))
                    group_data = group.scalars().first()

                    if group_data:
                        return GetGroup(
                            id=group_data.id,
                            name=group_data.name,
                            admin_id=group_data.admin_id,
                            users=[Person.from_dict(user) for user in group_data.users],
                            id_to_exclude=decoded_user_id
                        )

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None

    @classmethod
    async def generate_join_code(cls, group_id: int) -> GroupCodeResponse:
        delay = 270
        if group_id in cls.join_codes:
            current_time = datetime.now().time()
            time_remaining = cls.join_codes[group_id][1]

            time_difference = datetime.combine(datetime.min, current_time) - datetime.combine(datetime.min, time_remaining)
            delta_seconds = time_difference.total_seconds()

            sec = int(delay - delta_seconds)
            return GroupCodeResponse(code=cls.join_codes[group_id][0], life_time=sec)
        else:
            code = ''.join(random.choices(string.digits, k=6))
            creation_time = datetime.now().time()
            cls.join_codes[group_id] = [code, creation_time]

            async def delete_code_after_delay(group_id):
                await asyncio.sleep(delay)
                if group_id in cls.join_codes:
                    del cls.join_codes[group_id]

            asyncio.create_task(delete_code_after_delay(group_id))
            return GroupCodeResponse(code=code, life_time=delay)

    @classmethod
    async def join_group(cls, token: str, join_code: str) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                for group_id, val in cls.join_codes.items():
                    if str(val[0]) == str(join_code):
                        async with new_session() as session:
                            async with session.begin():
                                author = await UserDataManager.get_person_by_id(decoded_user_id)
                                group = await session.get(Group, group_id)

                                if author.to_dict() not in group.users:
                                    await session.execute(
                                        update(Group)
                                        .where(Group.id == group_id)
                                        .values(users=group.users + [author.to_dict()])
                                    )
                                    await session.commit()


                            await session.refresh(group)
                        del cls.join_codes[group_id]
                        return GetGroup(
                            id=group.id,
                            name=group.name,
                            admin_id=group.admin_id,
                            users=[Person.from_dict(user) for user in group.users],
                            id_to_exclude=decoded_user_id
                            )
                return None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None
    
    @classmethod
    async def change_admin(cls, token: str, group_id: int, new_admin_id: int) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    async with session.begin():
                        group = await session.get(Group, group_id)
                        if not group:
                            return None
                        else:
                            group.admin_id = new_admin_id
                            await session.refresh(group)
                            await session.commit()

                            return GetGroup(
                                id=group.id,
                                name=group.name,
                                admin_id=new_admin_id,
                                users=[Person.from_dict(user) for user in group.users],
                                id_to_exclude=new_admin_id
                            )      
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None
    
    @classmethod
    async def change_group_name(cls, token: str, group_id: int, new_name: str) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    async with session.begin():
                        group = await session.get(Group, group_id)
                        if not group:
                            return None
                        else:
                            group.name = new_name
                            await session.refresh(group)
                            await session.commit()

                            return GetGroup(
                                id=group.id,
                                name=new_name,
                                admin_id=group.admin_id,
                                users=[Person.from_dict(user) for user in group.users],
                                id_to_exclude=group.admin_id
                            )      
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None
    
    @classmethod
    async def remove_user_from_group(cls, token: str, group_id: int, user_id: int) -> Optional[GetGroup]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                async with new_session() as session:
                    async with session.begin():
                        group = await session.get(Group, group_id)

                        if group:
                            user_index = next((index for index, user in enumerate(group.users) if user['id'] == user_id), None)
                            if user_index is not None:
                                group.users.pop(user_index)
                                session.add(group)
                                await session.commit()
                                # delete from user info

                                return GetGroup(
                                    id=group.id,
                                    name=group.name,
                                    admin_id=group.admin_id,
                                    users=[Person.from_dict(user) for user in group.users],
                                    id_to_exclude=decoded_user_id
                                )
                            else:
                                return None
                        else:
                            return None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return None
