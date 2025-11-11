from app.entities.common.dao import BaseDAO
from app.entities.employeemeetings.models import EmployeeMeeting


class EmployeeMeetingsDAO(BaseDAO):
    model = EmployeeMeeting
