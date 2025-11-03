from app.common.dao import BaseDAO
from app.departments.models import Department


class DepartmentsDAO(BaseDAO):
    model = Department
