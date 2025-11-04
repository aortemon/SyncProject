from pydantic import Field
from app.common.schema import SchemaBase


class ReleaseBase(SchemaBase):
    name: str = Field(
        ...,
        description='Release name'
    )
    version: str = Field(
        ...,
        description='Release version',
        min_length=3
    )
    description: str = Field(
        ...,
        description='Release description'
    )
    status_id: int = Field(
        ...,
        description='Status ID'
    )


class SNewRelease(ReleaseBase):
    ...


class SUpdateRelease(ReleaseBase):
    id: int = Field(
        ...,
        description='ID of release to update'
    )
