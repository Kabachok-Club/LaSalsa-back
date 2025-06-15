from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.crud import (
    create_task,
    get_tasks_by_offset,
    delete_task,
    update_task,
    update_task_status,
    get_task_by_id,
)
from app.schemas import TaskCreate, TaskRead, TaskShort, TaskStatus, TaskID


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=201, response_model=TaskRead)
async def create_task_endpoint(
    task: TaskCreate, db: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task.
    """
    return await create_task(db, task)


@router.get("/", response_model=list[TaskShort])
async def get_tasks_endpoint(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    """
    Get tasks with pagination.
    """
    return await get_tasks_by_offset(db, offset, limit)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id_endpoint(
    task_id: int, db: AsyncSession = Depends(get_async_session)
):
    """
    Get a task by ID.
    """
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/")
async def delete_task_endpoint(
    task_id: TaskID, db: AsyncSession = Depends(get_async_session)
):
    """
    Delete a task by ID.
    """
    return await delete_task(db, task_id.id)


@router.put("/{task_id}/update", response_model=TaskRead)
async def update_task_endpoint(
    task_id: int, task_data: TaskCreate, db: AsyncSession = Depends(get_async_session)
):
    """
    Update a task by ID.
    """
    task = await update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/status", response_model=TaskRead)
async def update_task_status_endpoint(
    task_status: TaskStatus, db: AsyncSession = Depends(get_async_session)
):
    """
    Update the status of a task by ID.
    """
    task = await update_task_status(db, task_status.id, task_status.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
