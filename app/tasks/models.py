from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, created_at, int_pk, str256

if TYPE_CHECKING:
    from app.employees.models import Employee
    from app.projects.models import Project
    from app.statuses.models import Status
    from app.taskfiles.models import TaskFile


class Task(Base):
    id: Mapped[int_pk]
    creator_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    executor_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    created_at: Mapped[created_at]
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    name: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    creator: Mapped["Employee"] = relationship("Employee", foreign_keys=[creator_id])
    executor: Mapped["Employee"] = relationship("Employee", foreign_keys=[executor_id])
    status: Mapped["Status"] = relationship("Status")
    project: Mapped["Project"] = relationship("Project")
    status: Mapped["Status"] = relationship("Status")
    project: Mapped["Project"] = relationship("Project")

    task_files: Mapped[List["TaskFile"]] = relationship(
        "TaskFile", back_populates="task", lazy="selectin", cascade="all, delete-orphan"
    )
