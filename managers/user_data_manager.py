from db.user.user_database import User, new_session as new_user_session
from sqlalchemy import select
from schemes.person_scheme import Person

class UserDataManager:
    async def get_person_by_id(id: int) -> Person:
        user_session = new_user_session()
        try:
            user_stmt = select(User).where(User.id == id)
            user_result = await user_session.execute(user_stmt)
            user = user_result.scalars().first()

            if user:
                return Person(id=id, name=user.name, emoji=user.emoji)
            else:
                return 'not found'
        finally:
            await user_session.close()
