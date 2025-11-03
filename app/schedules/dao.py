from app.common.dao import BaseDAO
from app.schedules.models import Schedule


class SchedulesDAO(BaseDAO):
    model = Schedule
