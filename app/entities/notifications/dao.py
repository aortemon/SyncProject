from app.entities.common.dao import BaseDAO
from app.entities.notifications.models import Notification


class NotificationsDAO(BaseDAO):
    model = Notification
