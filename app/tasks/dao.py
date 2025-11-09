from typing import override

from app.common.dao import BaseDAO
from app.tasks.models import Task


class TasksDAO(BaseDAO):
    model = Task
