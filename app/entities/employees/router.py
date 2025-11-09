from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.employeedepartments.dao import EmployeeDepartmentsDAO
from app.entities.employees.dao import EmployeesDAO
from app.entities.employees.models import Employee
from app.entities.employees.schemas import SUpdateEmployee

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/all/")
async def get_all_users(user_data: Employee = Depends(require_access(ANY_USER))):
    return await EmployeesDAO.find_all()


@router.get("/get_by_id/")
async def get_user_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await EmployeesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )

    return result


@router.put("/update/")
async def update_project(
    response: Response,
    update: SUpdateEmployee,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    upd_dict = update.dict()
    departments_list = upd_dict.pop("departments")
    result = await EmployeesDAO.update(filter_by={"id": update.id}, **upd_dict)
    subquery_result = await EmployeeDepartmentsDAO.add_many(
        [
            {"department_id": x["id"], "employee_id": update.id, "office": x["office"]}
            for x in departments_list
        ]
    )
    if subquery_result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something wrong with departments",
        )

    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project was not updated. ID={update.id} not found",
        )
    return {"message": f"Project(id={update.id}) was updated successfully"}
    return {"message": f"Project(id={update.id}) was updated successfully"}
