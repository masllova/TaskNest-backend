from sqlalchemy import delete, select, update
from db.tasks_database import TaskData, new_session
from shemas.task_scemas import AddTask, GetTask
from sqlalchemy.exc import NoResultFound

class TaskRepository:
    @classmethod
    async def add_one(cls, data: AddTask) -> int:
        session = new_session()
        async with session.begin():
            task_dict = data.model_dump()
            task = TaskData(**task_dict)

            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_all(cls) -> list[GetTask]:
        session = new_session()
        async with session.begin():
            query = select(TaskData)
            result = await session.execute(query)
            tasks_models = result.scalars().all()
            tasks_scemas = [GetTask.model_validate(task.to_dict()) for task in tasks_models]
            return tasks_scemas

    @classmethod
    async def update_by_id(cls, task_id: int, data: AddTask) -> bool:
        session = new_session()
        async with session.begin():
            task_dict = data.model_dump()
            update_query = update(TaskData).where(TaskData.id == task_id).values(**task_dict)
            await session.execute(update_query)
            await session.commit()
            return True

    @classmethod
    async def delete_by_id(cls, task_id: int) -> bool:
        session = new_session()
        async with session.begin():
            try:
                query = select(TaskData).where(TaskData.id == task_id)
                result = await session.execute(query)
                task = result.scalars().one()

                delete_query = delete(TaskData).where(TaskData.id == task_id)
                await session.execute(delete_query)
                await session.commit()
                return True
            except NoResultFound:
                return False
