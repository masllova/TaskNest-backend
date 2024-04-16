from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional, List, Dict, Any
from sqlalchemy import JSON

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class TaskData(Model):
    __tablename__ = 'tasks'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    tasks_list: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(type_=JSON)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

async def create_tasks_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tasks_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)