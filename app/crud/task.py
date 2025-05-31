from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.schemas import TaskCreate, ProjectCreate
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

    print(f"Project: {project}")
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


async def get_tasks_by_offset(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[Task]:
    result = await db.execute(
        select(Task).offset(offset).limit(limit)
    )

    return result.scalars().all()

async def delete_task(db: AsyncSession, task_id: int) -> Task | None:
    task = await db.get(Task, task_id)
    if not task:
        return None

    await db.delete(task)
    await db.commit()
    return task