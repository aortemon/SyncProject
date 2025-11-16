from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.projects.dao import ProjectDAO
from app.entities.projects.schemas import SNewProject, SUpdateProject

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/all/")
async def get_all_projects(user_data: Employee = Depends(require_access(ANY_USER))):
    return await ProjectDAO.find_all()


@router.get("/get_by_id/")
async def get_project_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await ProjectDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_project(
    new_item: SNewProject,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    await ProjectDAO.add(**new_item.dict())
    return {"message": "New project was added successfully!"}


@router.put("/update/")
async def update_project(
    update: SUpdateProject,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    upd_dict = update.model_dump(exclude_none=True)
    id = upd_dict["id"]
    result = await ProjectDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"message": f"Project(id={id}) was updated successfully"}
