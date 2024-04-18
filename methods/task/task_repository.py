from sqlalchemy import delete, select, update, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from pymongo import MongoClient
from bson.objectid import ObjectId
from db.user.user_database import new_session  as new_user_session
from shemas.task_scemas import AddTask, GetTask, UpdateTask, Author
from managers.jwt_manager import JWTManager
from typing import Optional
import jwt

class TaskRepository:
    @classmethod
    async def add_one(cls, token: str, task: AddTask, id: Optional[int] = None) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                if id is not None:
                    user_id = id
                    name = get_user_name_by_id(user_id)
                    author = Author(id=user_id, name=name)
                else:
                    user_id = decoded_user_id
                    author = Author(id=user_id, name=None)

                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    tasks_count = len(task_data["tasks_list"])
                    task_dict = GetTask(id=tasks_count + 1, task=task, author=author, comments=[]).to_dict()
                    task_data["tasks_list"].append(task_dict)

                    collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                    return True
                else:
                    task_dict = GetTask(id=1, task=task, author=author, comments=[]).to_dict()
                    task_data = {"user_id": user_id, "tasks_list": [task_dict]}
                    collection.insert_one(task_data)
                    return True
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return False

    @classmethod
    async def get_all(cls, token: str) -> list[GetTask]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                task_data = collection.find_one({"user_id": decoded_user_id})

                if task_data:
                    tasks_models = task_data["tasks_list"]
                    tasks_scemas = [GetTask.from_dict(task) for task in tasks_models]
                    return tasks_scemas
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return []

    @classmethod
    async def update_by_id(cls, token: str, task_id: int, data: UpdateTask) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                task_data = collection.find_one({"user_id": decoded_user_id, "tasks_list.id": task_id})

                if task_data:
                    for task in task_data["tasks_list"]:
                        if task["id"] == task_id:
                            updated_task = GetTask.from_dict(task).update(data).to_dict()
                            task.update(updated_task)
                            break
                    collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                    return True
                else:
                    return False 
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return False

    @classmethod
    async def delete_by_id(cls, token: str, task_id: int) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                task_data = collection.find_one({"user_id": decoded_user_id, "tasks_list.id": task_id})

                if task_data:
                    updated_tasks_list = [task for task in task_data["tasks_list"] if task["id"] != task_id]
                    task_data["tasks_list"] = updated_tasks_list
                    collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                    return True
                else:
                    return False
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager>ITError
        return False

        async def get_user_name_by_id(id: int) -> str:
            user_session = new_user_session()
            try:
                user_stmt = select(User).where(User.id == user_create.id)
                user_result = await user_session.execute(user_stmt)
                user = user_result.scalars().first()

                if user:
                    return user.name
                else:
                    return 'not found'
            finally:
                await user_session.close()
