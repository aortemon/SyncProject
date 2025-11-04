from pydantic import BaseModel, Field, model_validator
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

    @model_validator(mode='after')
    def validate(self):
        if (
            self.starttime < self.lunchbreak_start <
            self.lunchbreak_end < self.endtime
        ):
            return self
        raise ValueError(
            'time fields are incorrect. Start times should '
            'come before end time.'
        )


class SNewWorkhour(WorkhourBase):
    ...


class SUpdateWorkhour(BaseModel):
    id: int = Field(
        ...,
        description='ID записи, которую нужно изменить',
    )
