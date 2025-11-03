from pydantic import Field
from datetime import date

from app.common.schema import SchemaBase


class TasksBase(SchemaBase):
    creator_id: int = Field(
        ...,
        description='ID создателя задачи'
    )
    executor_id: int = Field(
        ...,
        description='ID исполнителя задачи'
    )
    start_date: date = Field(
        ...,
        description='Дата начала выполнения задачи'
    )
    end_date: date = Field(
        ...,
        description='Дата окончания выполнения задачи'
    )
    name: str = Field(
        ...,
        description='Название задачи'
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


class SNewTask(TasksBase):
    ...


class SUpdateTask(TasksBase):
    id: int = Field(
        ...,
        description='ID задачи, который нужно обновить'
    )