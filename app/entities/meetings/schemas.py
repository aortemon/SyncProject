from datetime import datetime
from typing import List

from pydantic import Field

from app.entities.common.schema import SchemaBase, partial_model


class MeetingBase(SchemaBase):
    name: str = Field(
        ..., description="Meeting name/theme", min_length=3, max_length=30
    )
    description: str = Field(..., description="Meeting extra info", max_length=500)
    creator_id: int = Field(..., description="Creator ID")
    date: datetime = Field(
        ..., description="Date and time of meeting", examples=["2026-01-12 14:30:00"]
    )
    link: str = Field(..., description="Link on Meeting", max_length=256)
    employees: List[int] = Field(..., description="List of invited Employees ID ")


class SNewMeeting(MeetingBase): ...


@partial_model(required_fields=["id"])
class SUpdateMeeting(MeetingBase):
    id: int = Field(..., description="ID of department to update")
