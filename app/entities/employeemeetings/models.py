from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, empls_fk

if TYPE_CHECKING:
    from app.entities.employees.models import Employee
    from app.entities.meetings.models import Meeting


class EmployeeMeeting(Base):
    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"), nullable=False, primary_key=True
    )
    employee_id: Mapped[empls_fk]

    meeting: Mapped["Meeting"] = relationship(
        "Department", back_populates="employee_meetings"
    )

    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="employee_meetings"
    )
