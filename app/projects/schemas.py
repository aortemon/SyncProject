from pydantic import Field
from app.common.schema import SchemaBase


class ProjectBase(SchemaBase):
    name: str = Field(
        ...,
        description='Название проекта'
    )
    description: str = Field(
        ...,
        description='Описание проекта'
    )
    manager_id: int = Field(
        ...,
        description='ID менеджера проекта'
    )
    status_id: int = Field(
        ...,
        description='ID статуса проекта'
    )
    release_id: int = Field(
        ...,
        dsecription='ID релиза, которому принадлежит проект'
    )


class SNewProject(ProjectBase):
    ...


class SUpdateProject(ProjectBase):
    id: int = Field(
        ...,
        description='ID релиза, который нужно обновить'
    )
