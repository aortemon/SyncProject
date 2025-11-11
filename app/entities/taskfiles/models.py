from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base

if TYPE_CHECKING:
    from app.entities.files.models import File
    from app.entities.tasks.models import Task


class TaskFile(Base):
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False, primary_key=True
    )
    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"), nullable=False, primary_key=True
    )

    task: Mapped["Task"] = relationship("Task", back_populates="task_files")

    file: Mapped["File"] = relationship(
        "File", back_populates="task_files", lazy="selectin"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id=({self.task_id}, {self.file_id}))"
