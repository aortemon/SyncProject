from app.entities.common.dao import BaseDAO
from app.entities.workhours.models import WorkHour


class WorkHoursDAO(BaseDAO):
    model = WorkHour
