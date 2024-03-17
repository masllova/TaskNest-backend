from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional, List, Dict, Any
from sqlalchemy import JSON
from datetime import datetime
from shemas.comment_scemas import GetComment

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class TaskData(Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_completed: Mapped[bool]
    color_hex: Mapped[Optional[str]]
    author: Mapped[str]
    author_emoji: Mapped[str]
    creation_date: Mapped[datetime]
    deadline: Mapped[Optional[datetime]]
    description: Mapped[Optional[str]]
    comments: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(type_=JSON)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)