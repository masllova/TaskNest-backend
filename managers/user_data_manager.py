from db.user.user_database import User, new_session as new_user_session
from sqlalchemy import select

class UserDataManager:
    async def get_user_name_by_id(id: int) -> str:
        user_session = new_user_session()
        try:
            user_stmt = select(User).where(User.id == id)
            user_result = await user_session.execute(user_stmt)
            user = user_result.scalars().first()

            if user:
                return user.name
            else:
                return 'not found'
        finally:
            await user_session.close()
