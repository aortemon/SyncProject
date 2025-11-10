from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, empls_fk, int_pk, str256

if TYPE_CHECKING:
    from app.entities.employeedepartments.models import EmployeeDepartment
    from app.entities.employees.models import Employee


class Meeting(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    description: Mapped[str] = mapped_column(Text, nullable=True)
    creator_id: Mapped[empls_fk]
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    link: Mapped[str256]
