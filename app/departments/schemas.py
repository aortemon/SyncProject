from pydantic import Field

from app.common.schema import SchemaBase


class DepartmentBase(SchemaBase):
    name: str = Field(
        ...,
        description='Название отдела',
        min_length=3,
        max_length=30
    )
    lead_id: int = Field(
        ...,
        description='Идентификатор руководителя'
    )


class SNewDepartment(DepartmentBase):
    ...


class SUpdateDepartment(DepartmentBase):
    id: int = Field(
        ...,
        description='ID отдела, который нужно обновить'
    )
