from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )
    return result


@router.post("/add/")
async def add_project(
    response: Response,
    new_item: SNewProject,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    await ProjectDAO.add(**new_item.dict())
    return {"message": "New project was added successfully!"}


@router.put("/update/")
async def update_project(
    response: Response,
    update: SUpdateProject,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    result = await ProjectDAO.update(filter_by={"id": update.id}, **update.dict())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project was not updated. ID={update.id} not found",
        )
    return {"message": f"Project(id={update.id}) was updated successfully"}
