from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from database.model import Base, empls_fk, int_pk, str256

if TYPE_CHECKING:
    from app.employeedepartments.models import EmployeeDepartment
    from app.employees.models import Employee

class Department(Base):
    id: Mapped[int_pk]
    name: Mapped[str256]
    lead_id: Mapped[empls_fk]

    employee_departments: Mapped[List["EmployeeDepartment"]] = relationship(
        "EmployeeDepartment", back_populates="department"
    )

    lead: Mapped["Employee"] = relationship("Employee", lazy="selectin")
