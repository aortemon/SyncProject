from app.entities.common.dao import BaseDAO
from app.entities.employeedepartments.models import EmployeeDepartment


class EmployeeDepartmentsDAO(BaseDAO):
    model = EmployeeDepartment
