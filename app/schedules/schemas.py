from pydantic import Field
from app.common.schema import SchemaBase


class ScheduleBase(SchemaBase):
    sun_id: int = Field(
        ...,
        description='Sunday workhours'
    )
    mon_id: int = Field(
        ...,
        description='Monday workhours'
    )
    tue_id: int = Field(
        ...,
        description='Tuesday workhours'
    )
    wed_id: int = Field(
        ...,
        description='Wednesday workhours'
    )
    thu_id: int = Field(
        ...,
        description='Thursday workhours'
    )
    fri_id: int = Field(
        ...,
        description='Friday workhours'
    )
    sat_id: int = Field(
        ...,
        description='Saturday workhours'
    )


class SNewSchedule(ScheduleBase):
    ...


class SUpdateSchedule(ScheduleBase):
    id: int = Field(
        ...,
        description='IF of schedule to update'
    )
