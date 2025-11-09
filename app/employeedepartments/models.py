from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.departments.models import Department
from app.employees.models import Employee
from database.model import Base, str256


class EmployeeDepartment(Base):
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), nullable=False, primary_key=True
    )
    office: Mapped[str256]

    department: Mapped["Department"] = relationship(
        "Department", back_populates="employee_departments"
    )
    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="employee_departments"
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id=({self.department_id}, {self.employee_id}))"
        )
