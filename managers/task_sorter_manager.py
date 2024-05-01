import threading
import time

class TaskSorter:
    def __init__(self, collection):
        self.collection = collection
        self.sort_thread = threading.Thread(target=self.sort_tasks_foreground)

    def start_sorting(self):
        self.sort_thread.start()

    def sort_tasks_foreground(self):
        while True:
            time.sleep(60)  # Sorting will be performed every minute
            self.sort_tasks()

    def sort_tasks(self):
        tasks_data = self.collection.find()

        # Sorting tasks by user_id
        sorted_tasks_data = sorted(tasks_data, key=lambda x: x['user_id'])

        for user_tasks in sorted_tasks_data:
            # Sorting the user's tasks by id
            user_tasks['tasks_list'] = sorted(user_tasks['tasks_list'], key=lambda x: x['id'])

            # Sorting comments in each task by id
            for task in user_tasks['tasks_list']:
                task['comments'] = sorted(task['comments'], key=lambda x: x['id'])

            # Updating an entry in the collection
            self.collection.update_one({'_id': user_tasks['_id']}, {'$set': user_tasks})
