from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk, str256, created_at
from app.statuses.models import Status
from app.employees.models import Employee
from app.projects.models import Project
from datetime import datetime


class Task(Base):
    id: Mapped[int_pk]
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )
    executor_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )
    created_at: Mapped[created_at]
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    name: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("statuses.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )

    creator: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[creator_id]
    )
    executor: Mapped["Employee"] = relationship(
        "Employee",
        foreign_keys=[executor_id]
    )
    status: Mapped["Status"] = relationship("Status")
    project: Mapped["Project"] = relationship("Project")
