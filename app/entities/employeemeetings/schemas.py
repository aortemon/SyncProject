from pydantic import Field

from app.entities.common.schema import SchemaBase


class SAddNewEmployeeMeeting(SchemaBase):
    # Assuming that Meeting ID is known
    # Schema only for use inside /meetings/ route
    # Self own router is not required, all the needed logic is inside meetings router
    employee_id: int = Field(..., description="Employee")
