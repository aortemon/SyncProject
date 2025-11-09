from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, int_pk, str256

if TYPE_CHECKING:
    from app.entities.taskfiles.models import TaskFile


class File(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    source: Mapped[str256]
    extension: Mapped[str256]

    task_files: Mapped[List["TaskFile"]] = relationship(
        "TaskFile", back_populates="file"
    )
