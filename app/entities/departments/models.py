from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, load_only, relationship

from database.model import Base, empls_fk, int_pk, str256

if TYPE_CHECKING:
    from app.entities.employeedepartments.models import EmployeeDepartment
    from app.entities.employees.models import Employee


class Department(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    lead_id: Mapped[empls_fk]

    staff: Mapped[List["EmployeeDepartment"]] = relationship(
        "EmployeeDepartment", back_populates="department", lazy="selectin"
    )

    lead: Mapped["Employee"] = relationship("Employee")
