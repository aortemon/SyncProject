from app.common.dao import BaseDAO
from app.workhours.models import WorkHour


class WorkHoursDAO(BaseDAO):
    model = WorkHour
