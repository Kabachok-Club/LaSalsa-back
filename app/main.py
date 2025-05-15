from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="LaSalsa API", version="0.1.0")

from app.database import get_async_session
from app.crud import create_task
from app.models import Task
from app.schemas import TaskCreate

@app.get("/")
async def root():
    return {"message": "Welcome to LaSalsa API!"}


@app.post("/tasks/")
async def create_task_endpoint(task: TaskCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Create a new task.
    """
    return await create_task(db, task)