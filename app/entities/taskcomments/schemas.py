import json
from datetime import date
from typing import Annotated

from fastapi import Form, HTTPException
from pydantic import AfterValidator, Field, FutureDate, ValidationError, model_validator

from app.entities.common.schema import SchemaBase, Validate, as_form, partial_model


class TaskCommentBase(SchemaBase):
    task_id: int = Field(..., description="ID of task to which comment belongs")
    text: str = Field(..., description="Comment content", max_length=1500)


class SAddComment(TaskCommentBase): ...
