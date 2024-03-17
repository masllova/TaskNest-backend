from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from methods.task.task_router import router as tasks_router
from methods.comment.comment_router import router as comments_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('cleared')
    await create_tables()
    print('activation')
    yield
    print('shutdown')

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(comments_router)


