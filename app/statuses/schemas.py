from pydantic import Field
from app.common.schema import SchemaBase


class StatusBase(SchemaBase):
    alias: str = Field(
        ...,
        description='Описание статуса, например: "Приостановлен"',
        min_length=3,
        max_length=15
    )


class SNewStatus(StatusBase):
    ...


class SUpdateStatus(StatusBase):
    id: int = Field(
        ...,
        description='ID статуса, описание которого нужно обновить'
    )
