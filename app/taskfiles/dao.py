from app.common.dao import BaseDAO
from app.taskfiles.models import TaskFile


class TaskFilesDAO(BaseDAO):
    model = TaskFile
