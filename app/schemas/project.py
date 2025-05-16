from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ENUM for Project Status
class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# ENUM for Project Type
class ProjectType(str, Enum):
    KANBAN = "KANBAN"
    LIST = "LIST"
    GANTT = "GANTT"


# This is a Pydantic model for the Project schema
class ProjectBase(BaseModel):
    name: str = Field(..., title="Project Name", description="Name of the project")
    description: str = Field(..., title="Project Description", description="Description of the project")
    status: ProjectStatus = Field(ProjectStatus.INACTIVE, title="Project Status", description="Current status of the project")
    type: ProjectType = Field(ProjectType.LIST, title="Project Type", description="Type of the project")
    deadline: Optional[datetime] = Field(None, title="Deadline", description="Deadline for the project")


# This is a Pydantic model for the Project schema used for creating new projects - same as ProjectBase
class ProjectCreate(ProjectBase):
    name: str = Field(..., title="Project Name", description="Name of the project")
    description: Optional[str] = Field(None, title="Project Description", description="Description of the project")
    status: ProjectStatus = Field(ProjectStatus.INACTIVE, title="Project Status", description="Current status of the project")
    type: ProjectType = Field(ProjectType.LIST, title="Project Type", description="Type of the project")
    deadline: Optional[datetime] = Field(None, title="Deadline", description="Deadline for the project")