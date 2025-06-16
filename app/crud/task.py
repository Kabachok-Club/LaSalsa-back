from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, ProjectCreate
from app.common import TaskStatus

from app.crud.project import get_project_by_id, get_project_by_name, create_project

from datetime import datetime


async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    project_id = task.project_id
    project_name = task.project_name
    project = None

    if project_id:
        project = await get_project_by_id(db, project_id)

    if project_name:
        project = await get_project_by_name(db, project_name)
        if not project:
            project = await create_project(db, ProjectCreate(name=task.project_name))

    db_task = Task(
        name=task.name,
        description=task.description,
        planned_at=task.planned_at,
        created_at=datetime.now(),
        status=task.status,
        closed_at=task.closed_at,
        project_id=project.id if project else None,
    )

    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks_by_offset(
    db: AsyncSession, offset: int = 0, limit: int = 100
) -> list[Task]:
    result = await db.execute(select(Task).offset(offset).limit(limit))

    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int) -> Task | None:
    task = await db.get(Task, task_id)
    if not task:
        return None
    return task


async def delete_task(db: AsyncSession, task_id: int) -> Task | None:
    task = await db.get(Task, task_id)
    if not task:
        return None

    await db.delete(task)
    await db.commit()
    return task


async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskCreate
) -> Task | None:
    task = await db.get(Task, task_id)
    if not task:
        return None

    task.name = task_data.name
    task.description = task_data.description
    task.planned_at = task_data.planned_at
    task.closed_at = task_data.closed_at
    task.status = task_data.status
    task.project_id = task_data.project_id
    task.project_name = task_data.project_name
    await db.commit()
    await db.refresh(task)
    return task


async def update_task_status(
    db: AsyncSession, task_id: int, status: TaskStatus
) -> Task | None:
    task = await db.get(Task, task_id)
    if not task:
        return None

    task.status = status
    if status == TaskStatus.DONE:
        task.closed_at = datetime.now()
    else:
        task.closed_at = None
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks_by_project_id(
    db: AsyncSession, project_id: int, offset: int = 0, limit: int = 100
) -> list[Task]:
    result = await db.execute(
        select(Task).where(Task.project_id == project_id).offset(offset).limit(limit)
    )
    return result.scalars().all()