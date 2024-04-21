from sqlalchemy import select, insert, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from schemes.user_schemes import *
from db.user.authorization_database import Authorization, new_session as new_auth_session
from db.user.user_database import User, new_session as new_user_session
from passlib.hash import sha256_crypt
from managers.jwt_manager import JWTManager

class UserRepository:

    @classmethod
    async def check_user_authorization(cls, user_create: UserCreate) -> AuthResponse:
        user_session = new_user_session()
        auth_session = new_auth_session()
        try:
            user_stmt = select(User).where(User.mail == user_create.mail)
            user_result = await user_session.execute(user_stmt)
            user = user_result.scalars().first()

            if user is None:
                return AuthResponse(message=AuthStatus.NOT_FOUND.value)

            auth_stmt = select(Authorization.password).where(Authorization.id == user.id)
            auth_result = await auth_session.execute(auth_stmt)
            auth_record = auth_result.first()

            if auth_record is None:
                return AuthResponse(message=AuthStatus.NOT_FOUND.value)

            password_hash = auth_record[0]
            if sha256_crypt.verify(user_create.password, password_hash):
                return AuthResponse(
                    message=AuthStatus.SUCCESSFUL.value,
                    jwt=JWTManager.generate_token(user.id), 
                    user=GetUser.model_validate(user.to_dict())
                    )
            else:
                return AuthResponse(message=AuthStatus.INCORRECT_PASSWORD.value)
        finally:
            await user_session.close()
            await auth_session.close()

    @classmethod
    async def create_new_user(cls, user_create: UserCreate) -> AuthResponse:
        user_session = new_user_session()
        auth_session = new_auth_session()

        try:
            new_user = User(mail=user_create.mail)
            user_session.add(new_user)
            await user_session.flush()
            await user_session.commit()
            await user_session.refresh(new_user)

            user_id = new_user.id

            password_hash = sha256_crypt.encrypt(user_create.password)
            new_auth = Authorization(id=user_id, password=password_hash)
            auth_session.add(new_auth)
            await auth_session.flush()
            await auth_session.commit()

            return AuthResponse(
                message=AuthStatus.WELCOME.value,
                jwt=JWTManager.generate_token(new_user.id)
            )
        finally:
            await user_session.close()
            await auth_session.close()

    
    @classmethod
    async def get_user_info(cls, token: str, user_id: Optional[int] = None) -> Optional[GetUser]:
        if user_id:
            session = new_user_session()
            async with session.begin():
                query = select(User).where(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user:
                    user_info = GetUser.model_validate(user.to_dict())
                    return user_info
                return None
        else:
            try:
                decoded_user_id = JWTManager.decode_token(token)
                if decoded_user_id:
                    session = new_user_session()
                    async with session.begin():
                        query = select(User).where(User.id == decoded_user_id)
                        result = await session.execute(query)
                        user = result.scalars().first()
                        if user:
                            user_info = GetUser.model_validate(user.to_dict())
                            return user_info
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Expired token")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        return None

    @classmethod
    async def update_user_info(cls, token: str, data: UserBase) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                session = new_user_session()
                async with session.begin():
                    user_exists_query = exists().where(User.id == decoded_user_id)
                    user_exists = await session.scalar(select(user_exists_query))
                    
                    if not user_exists:
                        return False
                    
                    user_dict = data.dict()
                    update_query = update(User).where(User.id == decoded_user_id).values(**user_dict)
                    await session.execute(update_query)
                    await session.commit()
                    return True
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return False