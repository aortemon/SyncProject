from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.roles.models import Role
from app.entities.schedules.models import Schedule
from database.model import Base, int_pk, str256

if TYPE_CHECKING:
    from app.entities.employeedepartments.models import EmployeeDepartment


class Employee(Base):
    id: Mapped[int_pk]
    lname: Mapped[str256]
    fname: Mapped[str256]
    mname: Mapped[str256]
    dob: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    position: Mapped[str256] = mapped_column(nullable=True)
    phone: Mapped[str256]
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), default="1000", nullable=False)

    schedule: Mapped["Schedule"] = relationship("Schedule", lazy="selectin")
    role: Mapped["Role"] = relationship(lazy="selectin")

    employee_departments: Mapped[List["EmployeeDepartment"]] = relationship(
        "EmployeeDepartment",
        back_populates="employee",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    extend_existing = True
