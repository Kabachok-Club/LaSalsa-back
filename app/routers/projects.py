from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.crud import get_projects, get_tasks_by_project_id

router = APIRouter(prefix="/projects", tags=["projects"])
from app.schemas import ProjectBase, TaskShort

@router.get("/", response_model=list[ProjectBase])
async def get_projects_endpoint(db: AsyncSession = Depends(get_async_session)):
    """
    Get a list of projects.
    """
    # Placeholder for actual implementation
    projects = await get_projects(db)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    
    return projects


@router.get("/{project_id}/tasks", response_model=list[TaskShort])
async def get_tasks_by_project_endpoint(
    project_id: int, db: AsyncSession = Depends(get_async_session)
):
    """
    Get tasks by project ID.
    """
    # Placeholder for actual implementation
    tasks = await get_tasks_by_project_id(db, project_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this project")
    
    return tasks