from pymongo import MongoClient
from bson.objectid import ObjectId
from schemes.task_schemes import AddTask, GetTask, UpdateTask
from managers.jwt_manager import JWTManager
from managers.search_manager import SearchManager
from managers.user_data_manager import UserDataManager
from managers.task_collector_manager import TaskCollector
from typing import Optional
import jwt

class TaskRepository:
    @classmethod
    async def add_one(cls, token: str, task: AddTask, id: Optional[int]) -> Optional[GetTask]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient("mongodb://mongodb:27017/")
                db = client.test
                collection = db["tasksnest-tasks"]

                if id:
                    user_id = id
                    author = await UserDataManager.get_person_by_id(decoded_user_id)
                else:
                    user_id = decoded_user_id
                    author = None

                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    tasks_count = len(task_data["tasks_list"])
                    task = GetTask(id=tasks_count + 1, task=task, author=author, comments=[])
                    task_data["tasks_list"].append(task.to_dict())

                    collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                    client.close()
                    return task
                else:
                    task = GetTask(id=1, task=task, author=author, comments=[])
                    task_data = {"user_id": user_id, "tasks_list": [task.to_dict()]}
                    collection.insert_one(task_data)
                    client.close()
                    return task
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return None

    @classmethod
    async def get_all(cls, token: str, id: Optional[int] = None) -> list[GetTask]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                if id:
                    user_id = id
                else:
                    user_id = decoded_user_id
                return await TaskCollector.get_all(id=user_id)
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return []

    @classmethod
    async def update_by_id(cls, token: str, task_id: int, data: UpdateTask, id: Optional[int]) -> Optional[GetTask]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient("mongodb://mongodb:27017/")
                db = client.test
                collection = db["tasksnest-tasks"]

                if id:
                    another_author = True
                    user_id = id
                else:
                    user_id = decoded_user_id
                    another_author = False

                task_data = collection.find_one({"user_id": user_id, "tasks_list.id": task_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task_dict = task_data["tasks_list"][task_index]
                        task = GetTask.from_dict(task_dict)

                        if another_author:
                            if not TaskCollector.check_editing_rights(task=task, id=decoded_user_id):
                                client.close()
                                return None   
                        
                        updated_task = task.update(data)
                        task_dict.update(updated_task.to_dict())
                        collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                        client.close()
                        print(updated_task)
                        return updated_task
                return None
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return None

    @classmethod
    async def delete_by_id(cls, token: str, task_id: int, id: Optional[int] = None) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient("mongodb://mongodb:27017/")
                db = client.test
                collection = db["tasksnest-tasks"]

                if id:
                    another_author = True
                    user_id = id
                else:
                    user_id = decoded_user_id
                    another_author = False

                task_data = collection.find_one({"user_id": user_id, "tasks_list.id": task_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        if another_author:
                            task = GetTask.from_dict(task_data["tasks_list"][task_index])
                            if not TaskCollector.check_editing_rights(task=task, id=decoded_user_id):
                                client.close()
                                return False   
                            
                        task_data["tasks_list"].pop(task_index)
                        collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                        client.close()
                        return True
                client.close()
                return False
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return False
