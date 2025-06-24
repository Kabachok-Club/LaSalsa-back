from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

# This is a SQLAlchemy model for the Task table
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    planned_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    closed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=True)
    owner_uid: Mapped[str] = mapped_column(String, nullable=False, index=True)



