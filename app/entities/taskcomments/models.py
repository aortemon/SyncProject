from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, created_at, empls_fk, int_pk

if TYPE_CHECKING:
    from app.entities.employees.models import Employee
    from app.entities.tasks.models import Task


class TaskComment(Base):
    id: Mapped[int_pk]
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False, primary_key=False
    )
    author_id: Mapped[empls_fk]
    created_at: Mapped[created_at]
    text: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["Employee"] = relationship("Employee", lazy="selectin")
    task: Mapped["Task"] = relationship("Task")
