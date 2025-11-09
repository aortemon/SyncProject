from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )
    return result


@router.post("/add/")
async def add_department(
    response: Response,
    new_department: SNewDepartment,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    print(response)
    await DepartmentsDAO.add(**user_data.dict())
    return {"message": "New department was added successfully!"}


@router.put("/update/")
async def update_department(
    response: Response,
    update: SUpdateDepartment,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    result = await DepartmentsDAO.update(filter_by={"id": update.id}, **update.dict())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department was not updated. ID={update.id} not found",
        )
    return {"message": f"Department(id={update.id}) was updated successfully"}
