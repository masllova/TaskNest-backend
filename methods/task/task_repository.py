from pymongo import MongoClient
from bson.objectid import ObjectId
from schemes.task_schemes import AddTask, GetTask, UpdateTask
from schemes.person_scheme import Person
from managers.jwt_manager import JWTManager
from managers.search_manager import SearchManager
from managers.user_data_manager import UserDataManager
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

                if id:
                    user_id = id
                    info = await UserDataManager.get_user_name_and_emoji_by_id(decoded_user_id)
                    author = Person(id=decoded_user_id, name=info[1:], emoji=info[0])
                else:
                    user_id = decoded_user_id
                    author = None

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
    async def get_all(cls, token: str, id: Optional[int] = None) -> list[GetTask]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                if id:
                    user_id = id
                else:
                    user_id = decoded_user_id

                task_data = collection.find_one({"user_id": user_id})

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
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        updated_task = GetTask.from_dict(task).update(data).to_dict()
                        task.update(updated_task)
                        collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                        return True
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
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task_data["tasks_list"].pop(task_index)
                        collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                        return True
                return False
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager>ITError
        return False
