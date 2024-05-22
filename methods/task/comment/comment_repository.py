from pymongo import MongoClient
from typing import Optional
from bson.objectid import ObjectId
from schemes.comment_schemes import GetComment, UpdateComment
from schemes.task_schemes import GetTask
from managers.user_data_manager import UserDataManager
from managers.jwt_manager import JWTManager
from managers.search_manager import SearchManager
import jwt


class CommentRepository:
    @classmethod
    async def add_one(cls, token: str, task_id: int, desc: str, user_id: int) -> Optional[GetComment]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient("mongodb://root:example@mongo:27017")
                db = client.test
                collection = db["tasksnest-tasks"]

                author = await UserDataManager.get_person_by_id(decoded_user_id)
                
                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)
                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        comment_count=len(task["comments"])
                        comment = GetComment(id=comment_count+1, comment=UpdateComment(description=desc), author=author)

                        updated_task = GetTask.from_dict(task).add_comment(comment)
                        task.update(updated_task.to_dict())
                        collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})

                        client.close()
                        return comment
                else:  
                    client.close() 
                    return None
        except jwt.ExpiredSignatureError:
            raise JWTManager.ETError
        except jwt.InvalidTokenError:
            raise JWTManager.ITError
        return None


    @classmethod
    async def update_by_id(cls, token: str, user_id: int, task_id: int, comment_id: int, desc: str) -> Optional[GetComment]:
        try:
            decoded_user_id = JWTManager.decode_token(token)
            if decoded_user_id:
                client = MongoClient("mongodb://root:example@mongo:27017")
                db = client.test
                collection = db["tasksnest-tasks"]
                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)

                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        comment_index = SearchManager.search(task["comments"], "id", comment_id)

                        if comment_index is not None:
                            comment = GetComment.from_dict(task["comments"][comment_index]) 

                            if comment.author.id != decoded_user_id:
                                client.close()
                                return None
                            
                            updated_comment = comment.update(desc)
                            updated_task = GetTask.from_dict(task).update_comment(updated_comment).to_dict()
                            task.update(updated_task)
                            collection.update_one({"_id": ObjectId(task_data["_id"])}, {"$set": task_data})

                            client.close()
                            return updated_comment
                return None
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
                client = MongoClient("mongodb://root:example@mongo:27017")
                db = client.test
                collection = db["tasksnest-tasks"]
                task_data = collection.find_one({"user_id": user_id})

                if task_data:
                    task_index = SearchManager.search(task_data["tasks_list"], "id", task_id)

                    if task_index is not None:
                        task = task_data["tasks_list"][task_index]
                        comment_index = SearchManager.search(task["comments"], "id", comment_id)

                        if comment_index is not None:
                            comment = GetComment.from_dict(task["comments"][comment_index]) 

                            if comment.author.id != decoded_user_id:
                                client.close()
                                return False
                            
                            task["comments"].pop(comment_index)
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