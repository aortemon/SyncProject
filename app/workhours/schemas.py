from pydantic import BaseModel, Field
from datetime import time
from app.common.schema import SchemaBase


class WorkhourBase(SchemaBase):
    starttime: time = Field(
        ...,
        description='Время начала рабочего дня "HH:MM"'
    )
    endtime: time = Field(
        ...,
        description='Время конца рабочего дня "HH:MM"'
    )
    lunchbreak_start: time = Field(
        ...,
        description='Время начала обеденного перерыва "HH:MM"'
    )
    lunchbreak_end: time = Field(
        ...,
        description='Время конца обеденного перерыва "HH:MM"'
    )


class SNewWorkhour(WorkhourBase):
    ...


class SUpdateWorkhour(BaseModel):
    id: int = Field(
        ...,
        description='ID записи, которую нужно изменить',
    )
