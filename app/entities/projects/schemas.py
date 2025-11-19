from pydantic import Field

from app.entities.common.schema import SchemaBase, partial_model


class ProjectBase(SchemaBase):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    status_id: int = Field(..., description="Status ID")
    release_id: int = Field(..., description="Corresponding release ID")


class SNewProject(ProjectBase): ...


@partial_model(required_fields=["id"])
class SUpdateProject(ProjectBase):
    id: int = Field(..., description="ID of project to update")
    manager_id: int = Field(..., description="Manager's id")
