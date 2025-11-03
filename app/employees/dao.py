from app.common.dao import BaseDAO
from app.employees.models import Employee


class EmployeesDAO(BaseDAO):
    model = Employee
