from pydantic import Field

from app.entities.common.schema import SchemaBase, partial_model


class DepartmentBase(SchemaBase):
    name: str = Field(..., description="Department name", min_length=3, max_length=30)
    lead_id: int = Field(..., description="Leader's ID")


class SNewDepartment(DepartmentBase): ...


@partial_model(exclude_fields=["id"])
class SUpdateDepartment(DepartmentBase):
    id: int = Field(..., description="ID of department to update")
