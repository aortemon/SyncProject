from pydantic import (
    Field,
    FutureDate,
    model_validator,
    AfterValidator
)
from datetime import date
from typing import Annotated

from app.common.schema import SchemaBase, Validate


def validate_future_or_now(v: date) -> date:
    if v < date.today():
        raise ValueError('date can\'t be in the past')
    return v


FutureOrNowDate = Annotated[date, AfterValidator(validate_future_or_now)]


class TasksBase(SchemaBase):
    creator_id: int = Field(
        ...,
        description='ID создателя задачи'
    )
    executor_id: int = Field(
        ...,
        description='ID исполнителя задачи'
    )
    start_date: FutureOrNowDate = Field(
        ...,
        description='Дата начала выполнения задачи'
    )
    end_date: FutureDate = Field(
        ...,
        description='Дата окончания выполнения задачи'
    )
    name: str = Field(
        ...,
        description='Название задачи',
        min_length=3,
        max_length=30
    )
    description: str = Field(
        ...,
        description='Описание задачи'
    )
    status_id: int = Field(
        ...,
        description='ID статуса задачи'
    )
    project_id: int = Field(
        ...,
        description='ID проекта, которому принадлежит задача'
    )

    @model_validator(mode='after')
    def validate_start_end_dates(self):
        return Validate.dates_range(
            self,
            self.start_date,
            self.end_date,
            msg_on_error='start_date should come before end_date.'
        )


class SNewTask(TasksBase):
    ...


class SUpdateTask(TasksBase):
    id: int = Field(
        ...,
        description='ID задачи, который нужно обновить'
    )