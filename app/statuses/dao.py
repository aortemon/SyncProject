from app.common.dao import BaseDAO
from app.statuses.models import Status


class StatusesDAO(BaseDAO):
    model = Status
