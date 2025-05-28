from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.crud import create_task, get_tasks_by_offset
from app.schemas import TaskCreate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LaSalsa API", version="0.1.0")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to LaSalsa API!"}


@app.post("/tasks/")
async def create_task_endpoint(task: TaskCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Create a new task.
    """
    return await create_task(db, task)


@app.get("/tasks/")
async def get_tasks_endpoint(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    """
    Get tasks with pagination.
    """
    return await get_tasks_by_offset(db, offset, limit)