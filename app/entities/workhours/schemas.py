from datetime import time

from pydantic import BaseModel, Field, model_validator

from app.entities.common.schema import SchemaBase, partial_model


class WorkhourBase(SchemaBase):
    starttime: time = Field(..., description='Start time of workday "HH:MM"')
    endtime: time = Field(..., description='End time of workday "HH:MM"')
    lunchbreak_start: time = Field(..., description='Lunchbreak start time "HH:MM"')
    lunchbreak_end: time = Field(..., description='Lunchbreak end time "HH:MM"')

    @model_validator(mode="after")
    def validate(self):
        if self.starttime < self.lunchbreak_start < self.lunchbreak_end < self.endtime:
            return self
        raise ValueError(
            "time fields are incorrect. Start times should " "come before end time."
        )


class SNewWorkhour(WorkhourBase): ...


@partial_model(required_fields=["id"])
class SUpdateWorkhour(BaseModel):
    id: int = Field(
        ...,
        description="ID of workhour to update",
    )
