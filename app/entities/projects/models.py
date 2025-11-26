from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.employees.models import Employee
from app.entities.releases.models import Release
from app.entities.statuses.models import Status
from database.model import Base, created_at, empls_fk, int_pk, str256

if TYPE_CHECKING:
    from app.entities.tasks.models import Task


class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[created_at]
    manager_id: Mapped[empls_fk]
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    release_id: Mapped[int] = mapped_column(ForeignKey("releases.id"), nullable=False)

    manager: Mapped["Employee"] = relationship("Employee", lazy="selectin")
    status: Mapped["Status"] = relationship("Status", lazy="selectin")
    release: Mapped["Release"] = relationship(
        "Release", back_populates="projects", lazy="selectin"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="project", lazy="selectin"
    )
