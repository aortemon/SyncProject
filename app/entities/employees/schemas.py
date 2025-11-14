from datetime import date, timedelta
from typing import List

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


@partial_model(exclude_fields=["id"])
class SUpdateEmployee(EmployeeBase):
    id: int = Field(..., description="ID of project to update")
