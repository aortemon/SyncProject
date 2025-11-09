from app.entities.common.dao import BaseDAO
from app.entities.taskfiles.models import TaskFile


class TaskFilesDAO(BaseDAO):
    model = TaskFile
