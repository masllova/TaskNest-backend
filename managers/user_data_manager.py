from db.user.user_database import User, new_session as new_user_session
from sqlalchemy import select
from typing import Optional
from schemes.person_scheme import Person

class UserDataManager:
    async def get_person_by_id(id: int) -> Optional[Person]:
        user_session = new_user_session()
        try:
            user_stmt = select(User).where(User.id == id)
            user_result = await user_session.execute(user_stmt)
            user = user_result.scalars().first()

            if user:
                return Person(id=id, name=user.name, emoji=user.emoji)
            else:
                return None
        finally:
            await user_session.close()

    async def change_group_info(user_id: int, group_id: Optional[int]):
        user_session = new_user_session()
        try:
            user_stmt = select(User).where(User.id == user_id)
            user_result = await user_session.execute(user_stmt)
            user = user_result.scalars().first()

            if user:
                user.group_id = group_id
                await user_session.flush()
                await user_session.commit()
        finally:
            await user_session.close()
