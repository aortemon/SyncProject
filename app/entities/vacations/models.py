from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.model import Base, empls_fk, int_pk

if TYPE_CHECKING:
    from app.entities.employees.models import Employee


class Vacation(Base):
    id: Mapped[int_pk]
    employee_id: Mapped[empls_fk]
    start_day: Mapped[date] = mapped_column(Date, nullable=False)
    end_day: Mapped[date] = mapped_column(Date, nullable=False)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="vacations")
