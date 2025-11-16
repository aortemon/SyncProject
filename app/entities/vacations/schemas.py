from datetime import date, timedelta

from pydantic import Field, model_validator

from app.entities.common.schema import SchemaBase, Validate, partial_model


class VacationBase(SchemaBase):
    employee_id: int = Field(..., description="Employee ID")
    start_day: date = Field(..., description="Date when vacation starts")
    end_day: date = Field(..., description="Date when vacation ends")

    @model_validator(mode="after")
    def validate(self):

        return Validate.dates_range(
            self,
            self.start_day,
            self.end_day,
            min_delta=timedelta(days=1),
            max_delta=timedelta(days=365),
        )


class SNewVacation(VacationBase): ...


@partial_model(required_fields=["id"])
class SUpdateVacation(VacationBase):
    id: int = Field(..., description="ID of department to update")
