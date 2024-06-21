from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from pymongo import MongoClient
from managers.task_sorter_manager import TaskSorter
from db.user.authorization_database import create_authorization_tables, delete_authorization_tables
from db.user.user_database import create_user_tables, delete_user_tables
from db.group_database import create_group_tables, delete_group_tables
from methods.task.task_router import router as tasks_router
from methods.task.comment.comment_router import router as comments_router
from methods.user.user_router import router as user_router
from methods.group.group_router import router as group_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_authorization_tables()
    await create_user_tables()
    await create_group_tables()
    # await delete_authorization_tables()
    # await delete_user_tables()
    # await delete_group_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(user_router)
app.include_router(group_router)

client = MongoClient("mongodb+srv://tasksnest:Akya3QlucuUehnFj@cluster0.emdxmco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['taskdb']
collection = db['task']

sorter = TaskSorter(collection)

sorter_thread = threading.Thread(target=sorter.start_sorting)
sorter_thread.daemon = True  # Set the background thread as a daemon so that it ends when the program ends
sorter_thread.start()



