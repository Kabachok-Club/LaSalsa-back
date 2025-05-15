from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.schemas import ProjectCreate

from datetime import datetime

async def create_project(db: AsyncSession, project: ProjectCreate) -> Project:
    print(f"Creating project: {project}")
    db_project = Project(
        name=project.name,
        description=project.description,
        created_at=datetime.now(),
        type=project.type,
        deadline=project.deadline,
        status=project.status,
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def get_project_by_id(db: AsyncSession, project_id: int) -> Project | None:
    return await db.get(Project, project_id)

async def get_project_by_name(db: AsyncSession, project_name: str) -> Project | None:
    result = await db.execute(
        select(Project).where(Project.name == project_name)
    )

    return result.scalars().first()