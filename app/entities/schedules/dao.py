from app.entities.common.dao import BaseDAO
from app.entities.schedules.models import Schedule


class SchedulesDAO(BaseDAO):
    model = Schedule
