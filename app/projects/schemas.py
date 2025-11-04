from pydantic import Field
from app.common.schema import SchemaBase


class ProjectBase(SchemaBase):
    name: str = Field(
        ...,
        description='Project name'
    )
    description: str = Field(
        ...,
        description='Project description'
    )
    manager_id: int = Field(
        ...,
        description='Manager\'s id'
    )
    status_id: int = Field(
        ...,
        description='Status ID'
    )
    release_id: int = Field(
        ...,
        dsecription='Corresponding release ID'
    )


class SNewProject(ProjectBase):
    ...


class SUpdateProject(ProjectBase):
    id: int = Field(
        ...,
        description='ID of project to update'
    )
