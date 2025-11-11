from app.entities.common.dao import BaseDAO
from app.entities.departments.models import Department


class DepartmentsDAO(BaseDAO):
    model = Department
