from pymongo import MongoClient
from schemes.task_schemes import GetTask
from schemes.user_schemes import GetUser

class TaskCollector:
    @staticmethod
    async def get_all(id: int) -> list[GetTask]:
        client = MongoClient()
        db = client.test
        collection = db["tasksnest-tasks"]

        task_data = collection.find_one({"user_id": id})

        if task_data:
            tasks_models = task_data["tasks_list"]
            tasks_scemas = [GetTask.from_dict(task) for task in tasks_models]
            client.close()
            return tasks_scemas
        else:
            client.close()
            return []

    def check_editing_rights(task: GetTask, id: int) -> bool:
        if task.author:
            if task.author.id == id:
                return True
        return False
            

    def fill_user_with_task_statistics(user: GetUser, tasks: list[GetTask]) -> GetUser:
        user.completed_tasks = sum(1 for task in tasks if task.is_completed)
        user.completed_personal_tasks = sum(1 for task in tasks if task.is_completed and task.author is None)
        user.completed_external_tasks = sum(1 for task in tasks if task.is_completed and task.author is not None)

        user.pending_tasks = sum(1 for task in tasks if not task.is_completed)
        user.pending_personal_tasks = sum(1 for task in tasks if not task.is_completed and task.author is None)
        user.pending_external_tasks = sum(1 for task in tasks if not task.is_completed and task.author is not None)

        return user