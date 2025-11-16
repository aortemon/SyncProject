import json
from datetime import date
from typing import Annotated

from fastapi import Form, HTTPException
from pydantic import AfterValidator, Field, FutureDate, ValidationError, model_validator

from app.entities.common.schema import SchemaBase, Validate, as_form, partial_model


def validate_future_or_now(v: date) -> date:
    if v < date.today():
        raise ValueError("date can't be in the past")
    return v


FutureOrNowDate = Annotated[date, AfterValidator(validate_future_or_now)]


class TasksBase(SchemaBase):
    executor_id: int | None = None  # Field(..., description="Executor's ID")
    start_date: FutureOrNowDate = Field(..., description="Start date of task execution")
    end_date: FutureDate = Field(..., description="End date of task execution")
    name: str = Field(..., description="Task name", min_length=3, max_length=30)
    description: str = Field(..., description="Task description")
    status_id: int = Field(..., description="Status ID")
    project_id: int = Field(..., description="Project ID")

    @model_validator(mode="after")
    def validate_start_end_dates(self):
        return Validate.dates_range(
            self,
            self.start_date,
            self.end_date,
            msg_on_error="start_date should come before end_date.",
        )


@as_form
class SNewTask(TasksBase):
    ...

    @classmethod
    def as_form(cls, task_data: str = Form(..., description="JSON таски")):
        try:
            data_dict = json.loads(task_data)
            return cls(**data_dict)
        except (json.JSONDecodeError, ValidationError) as e:
            raise HTTPException(400, f"Invalid task data: {e}")


@partial_model(required_fields=["id"])
class SUpdateTask(TasksBase):
    id: int = Field(..., description="ID of task to update")
