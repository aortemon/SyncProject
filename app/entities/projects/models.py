from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.employees.models import Employee
from app.entities.releases.models import Release
from app.entities.statuses.models import Status
from database.model import Base, created_at, empls_fk, int_pk, str256


class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[created_at]
    manager_id: Mapped[empls_fk]
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    release_id: Mapped[int] = mapped_column(ForeignKey("releases.id"), nullable=False)

    manager: Mapped["Employee"] = relationship("Employee")
    status: Mapped["Status"] = relationship("Status")
    release: Mapped["Release"] = relationship("Release")
    release: Mapped["Release"] = relationship("Release")
