from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, String

engine = create_async_engine("sqlite+aiosqlite:///authorization.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class Authorization(Model):
    __tablename__ = 'authorization'

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str]
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


async def create_authorization_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_authorization_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)