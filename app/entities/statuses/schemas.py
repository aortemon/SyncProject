from pydantic import Field

from app.entities.common.schema import SchemaBase


class StatusBase(SchemaBase):
    alias: str = Field(
        ..., description="Status description", min_length=3, max_length=15
    )


class SNewStatus(StatusBase): ...


class SUpdateStatus(StatusBase):
    id: int = Field(..., description="ID of status to update")
