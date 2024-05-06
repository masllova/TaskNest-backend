from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Dict, Any

engine = create_async_engine("sqlite+aiosqlite:///groups.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class Group(Model):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    admin_id: Mapped[int]
    users: Mapped[List[Dict[str,Any]]] = mapped_column(type_=JSON)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "admin_id": self.admin_id,
            "users": self.users
            }

async def create_group_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_group_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)