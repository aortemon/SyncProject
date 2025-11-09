from app.entities.common.dao import BaseDAO
from app.entities.employees.models import Employee


class EmployeesDAO(BaseDAO):
    model = Employee
