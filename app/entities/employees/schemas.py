from datetime import date, time, timedelta
from typing import List, Tuple

from pydantic import EmailStr, Field, PastDate, field_validator

from app.entities.common.schema import SchemaBase, Validate, partial_model
from app.entities.employeedepartments.schemas import SAddEmployeeDepartment


class EmployeeBase(SchemaBase):

    lname: str = Field(
        ..., description="Last name", examples=["Пупкин"], min_length=3, max_length=50
    )
    fname: str = Field(
        ..., description="First name", examples=["Василий"], min_length=3, max_length=50
    )
    mname: str = Field(
        ...,
        description="Middle name",
        examples=["Акакиевич"],
        min_length=3,
        max_length=50,
    )
    dob: PastDate = Field(
        ...,
        description="Date of birth. Format: YYYY-MM-DD",
        le=date.today() - timedelta(days=365 * 16),
    )
    schedule_id: int = Field(..., description="Schedule ID")
    position: str = Field(..., description="Position of employee")
    role_id: int = Field(..., description="Role ID")
    departments: List[SAddEmployeeDepartment] = Field(
        ..., description="List of departments' IDs where employee works"
    )
    phone: str = Field(
        ...,
        description="Phone number",
        examples=["+79051534857"],
        min_length=12,
        max_length=12,
    )
    email: EmailStr = Field(..., description="Email", min_length=3, max_length=50)
    password: str = Field(
        ...,
        description="Password",
        min_length=12,
        max_length=48,
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        return Validate.phone(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return Validate.password(value)


@partial_model(required_fields=["id"])
class SUpdateEmployee(EmployeeBase):
    id: int = Field(..., description="ID of project to update")


class SCalendarDate(SchemaBase):
    day: date = Field(...)
    is_vacation: bool = Field(
        ..., description="True, if employee is in a vacation", examples=[False, True]
    )
    is_weekend: bool = Field(
        ..., description="True if employee is in the weekend", examples=[False, True]
    )
    task_deadlines: List[Tuple[str, str]] = Field(
        ...,
        description="List of tuples contain name of task and links to it",
        examples=[
            [
                ("Add validators to admin schemas", "/get_task_by_id/228"),
                ("Fix db Integrity Error on do_backup() call", "/get_task_by_id/578"),
            ]
        ],
    )
    timesheet: List[Tuple[time, str, str | None]] = Field(
        ...,
        description="List of tuples sorted by time containing triplets of time, activity and, optionally, link to activity",
        examples=[
            [
                ("08:00", "Start of the workday", ""),
                ("15:30", 'Meeting "Yellow Boletus in USA"', "/get_meeting_by_id/1488"),
            ]
        ],
    )
    active_tasks: List[Tuple[str, str]] = Field(
        ...,
        description="List of tuples comtaining pairs of task and link to it",
        examples=[
            [
                ("Fix pupku and zalupku", "/get_task_by_id/8064523"),
                ("Upload trans furry porn to source.unn.ru", "/get_task_by_id/2561024"),
            ]
        ],
    )
