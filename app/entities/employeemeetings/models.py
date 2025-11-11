from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base

if TYPE_CHECKING:
    from app.entities.employees.models import Employee
    from app.entities.meetings.models import Meeting


class EmployeeMeeting(Base):
    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"), nullable=False, primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), nullable=False, primary_key=True
    )

    meeting: Mapped["Meeting"] = relationship(
        "Meeting", back_populates="employee_meetings"
    )

    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="employee_meetings"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id=({self.meeting_id}, {self.employee_id}))"
