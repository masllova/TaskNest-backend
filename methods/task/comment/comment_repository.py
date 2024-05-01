from pymongo import MongoClient
from bson.objectid import ObjectId
from schemes.comment_schemes import GetComment, UpdateComment
from schemes.task_schemes import GetTask
from schemes.person_scheme import Person
from managers.user_data_manager import UserDataManager
from managers.jwt_manager import JWTManager
from managers.search_manager import SearchManager
import jwt


class CommentRepository:
    @classmethod
    async def add_one(cls, token: str, task_id: int, desc: str, user_id: int) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                info = await UserDataManager.get_user_name_and_emoji_by_id(decoded_user_id)
                author = Person(id=decoded_user_id, name=info[1:], emoji=info[0])

                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task = task_data["tasks_list"][task_index] # проблема тут
                        comment_count=len(task["comments"])
                        comment = GetComment(id=comment_count+1, comment=UpdateComment(description=desc), author=author)
                        updated_task = GetTask.from_dict(task).add_comment(comment).to_dict()
                        task.update(updated_task)
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
    async def update_by_id(cls, token: str, user_id: int, task_id: int, comment_id: int, desc: str) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        comment_index = SearchManager.search(task["comments"], "id", comment_id)
                        if comment_index is not None:
                            comment = task["comments"][comment_index]
                            updated_comment = GetComment.from_dict(comment).update(desc)
                            updated_task = GetTask.from_dict(task).update_comment(updated_comment).to_dict()
                            task.update(updated_task)
                            collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                            return True
                return False
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return False

    @classmethod
    async def delete_by_id(cls, token: str, user_id: int, task_id: int, comment_id: int) -> bool:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient()
                db = client.test
                collection = db["tasksnest-tasks"]

                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        comment_index = SearchManager.search(task["comments"], "id", comment_id)
                        if comment_index is not None:
                            task["comments"].pop(comment_index)
                            collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})
                            return True
                return False
                client.close()
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return False