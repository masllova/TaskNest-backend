from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import date

engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str]
    name: Mapped[Optional[str]]
    emoji: Mapped[Optional[str]]
    birthday: Mapped[Optional[date]]
    status: Mapped[Optional[str]]

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

async def create_user_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_user_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
