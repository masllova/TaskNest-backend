from db.group_database import Group, new_session
# from sqlalchemy import select, update, exists
from managers.jwt_manager import JWTManager
from schemes.group_scheme import *


class GroupRepository:

    @classmethod
    async def create_new_group(cls, token: str, name: str) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                session = new_session()
                async with session.begin():
                    new_group = Group(name=name, admin_id=decoded_user_id, users=[])
                    session.add(new_group)
                    await session.flush()
                    await session.commit()
                    await session.refresh(new_group)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return False