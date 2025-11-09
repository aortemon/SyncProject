from app.entities.common.dao import BaseDAO
from app.entities.tasks.models import Task


class TasksDAO(BaseDAO):
    model = Task
