from pydantic import Field
from app.common.schema import SchemaBase


class SAddEmployeeDepartment(SchemaBase):
    id: int = Field(
        ...,
        description='Department ID'
    )
    office: str = Field(
        ...,
        description=(
            "Office where employee work in"
            " department, e. g. 'Каб. 228'"
        )
    )
