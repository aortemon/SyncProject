from datetime import date

from pydantic import Field

from app.entities.common.schema import SchemaBase


class VacationBase(SchemaBase):
    employee_id: int = Field(..., description="Employee ID")
    start_day: date = Field(..., description="Date when vacation starts")
    end_day: date = Field(..., description="Date when vacation ends")


class SNewVacation(VacationBase): ...


class SUpdateVacation(VacationBase):

    id: int = Field(..., description="ID of department to update")
