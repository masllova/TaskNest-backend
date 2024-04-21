from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.user.authorization_database import create_authorization_tables, delete_authorization_tables
from db.user.user_database import create_user_tables, delete_user_tables
from methods.task.task_router import router as tasks_router
from methods.task.comment.comment_router import router as comments_router
from methods.user.user_router import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_authorization_tables()
    # await delete_user_tables()
    # print('cleared')
    await create_authorization_tables()
    await create_user_tables()
    print('activation')
    yield
    print('shutdown')

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(user_router)



