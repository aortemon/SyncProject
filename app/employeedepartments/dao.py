from app.common.dao import BaseDAO
from app.employeedepartments.models import EmployeeDepartment


class EmployeeDepartmentsDAO(BaseDAO):
    model = EmployeeDepartment
