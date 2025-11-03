from pydantic import Field
from app.common.schema import SchemaBase


class ScheduleBase(SchemaBase):
    sun_id: int = Field(
        ...,
        description='Рабочий график воскресенья'
    )
    mon_id: int = Field(
        ...,
        description='Рабочий график понедельника'
    )
    tue_id: int = Field(
        ...,
        description='Рабочий график вторника'
    )
    wed_id: int = Field(
        ...,
        description='Рабочий график среды'
    )
    thu_id: int = Field(
        ...,
        description='Рабочий график четверга'
    )
    fri_id: int = Field(
        ...,
        description='Рабочий график пятницы'
    )
    sat_id: int = Field(
        ...,
        description='Рабочий график субботы'
    )


class SNewSchedule(ScheduleBase):
    ...


class SUpdateSchedule(ScheduleBase):
    id: int = Field(
        ...,
        description='ID расписания, которое нужно обновить'
    )
