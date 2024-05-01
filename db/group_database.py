from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Dict
from datetime import date

engine = create_async_engine("sqlite+aiosqlite:///groups.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class Group(Model):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    admin_id: Mapped[int]
    users: Mapped[List[Dict[str:any]]]

    def to_dict(self):
        users = [{'id': user['id'], 'name': user['name'], 'emoji': user['emoji']} for user in self.users]
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'users'} | {'users': users}

async def create_group_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_group_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)