from app.entities.common.dao import BaseDAO
from app.entities.statuses.models import Status


class StatusesDAO(BaseDAO):
    model = Status
