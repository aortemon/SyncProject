from pydantic import Field
from app.common.schema import SchemaBase


class ReleaseBase(SchemaBase):
    name: str = Field(
        ...,
        description='Название релиза'
    )
    version: str = Field(
        ...,
        description='Версия релиза'
    )
    description: str = Field(
        ...,
        description='Описание релиза'
    )
    status_id: int = Field(
        ...,
        description='ID статуса проекта'
    )


class SNewRelease(ReleaseBase):
    ...


class SUpdateRelease(ReleaseBase):
    id: int = Field(
        ...,
        description='ID релиза, который нужно обновить'
    )
