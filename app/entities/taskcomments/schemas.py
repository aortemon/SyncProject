from pydantic import Field

from app.entities.common.schema import SchemaBase


class TaskCommentBase(SchemaBase):
    task_id: int = Field(..., description="ID of task to which comment belongs")
    text: str = Field(..., description="Comment content", max_length=1500)


class SAddComment(TaskCommentBase): ...
