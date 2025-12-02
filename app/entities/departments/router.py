from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.departments.dao import DepartmentsDAO
from app.entities.departments.schemas import SNewDepartment, SUpdateDepartment
from app.entities.employees.models import Employee

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/all/")
async def get_all_departments(user_data: Employee = Depends(require_access(ANY_USER))):
    return await DepartmentsDAO.find_all()


@router.get("/get_by_id/")
async def get_department_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await DepartmentsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_department(
    new_department: SNewDepartment,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await DepartmentsDAO.add(**new_department.model_dump())
    return {"msg": "Successfully added!"}


@router.put("/update/")
async def update_department(
    update: SUpdateDepartment,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    upd_dict = update.model_dump(exclude_none=True)
    id = upd_dict["id"]
    result = await DepartmentsDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"msg": f"Department(id={id}) was updated successfully"}
