from app.entities.common.dao import BaseDAO
from app.entities.taskcomments.models import TaskComment


class TaskCommentDAO(BaseDAO):
    model = TaskComment
