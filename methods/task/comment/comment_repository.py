from sqlalchemy import delete, select, update
from db.tasks_database import TaskData, new_session
from shemas.comment_scemas import AddComment, GetComment, UpdateComment
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import json

class CommentRepository:
    @classmethod
    async def add_one(cls, data: AddComment, task_id: int) -> int:
        session = new_session()
        async with session.begin():
            query = select(TaskData).where(TaskData.id == task_id)
            result = await session.execute(query)
            task = result.scalars().one()
            id = 0
            if task.comments:
                id = len(task.comments)
            
            comment_dict = {
                'id': id,
                'author': data.author,
                'author_emoji': data.author_emoji,
                'creation_date': data.creation_date,
                'description': data.description,
                'is_updated': False
            }

            if task.comments is None:
                task.comments = [comment_dict]
            else:
                task.comments.append(comment_dict)

            update_query = update(TaskData).where(TaskData.id == task_id).values(comments=task.comments)
            await session.execute(update_query)
            await session.commit()
            return id


    @classmethod
    async def update_by_id(cls, task_id: int, comment_id: int, data: UpdateComment) -> bool:
        session = new_session()
        async with session.begin():
            query = select(TaskData).where(TaskData.id == task_id)
            result = await session.execute(query)
            task = result.scalars().one()

            if task and task.comments:
                for comment in task.comments:
                    if comment['id'] == comment_id:
                        comment['creation_date'] = data.creation_date
                        comment['description'] = data.description
                        comment['is_updated'] = True

                        update_query = update(TaskData).where(TaskData.id == task_id).values(comments=task.comments)
                        await session.execute(update_query)

                        await session.commit()
                        return True
        return False

    @classmethod
    async def delete_by_id(cls, task_id: int, comment_id: int) -> bool:
        session = new_session()
        async with session.begin():
            query = select(TaskData).where(TaskData.id == task_id)
            result = await session.execute(query)
            task = result.scalars().one()

            if task and task.comments:
                for index, comment in enumerate(task.comments):
                    if comment['id'] == comment_id:
                        del task.comments[index]

                        update_query = update(TaskData).where(TaskData.id == task_id).values(comments=task.comments)
                        await session.execute(update_query)

                        await session.commit()
                        return True
        return False


