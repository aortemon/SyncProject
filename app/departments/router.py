from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.departments.dao import DepartmentsDAO
from app.departments.schemas import SNewDepartment, SUpdateDepartment
from app.employees.models import Employee
from app.employees.dependencies import get_current_admin_user


router = APIRouter(prefix='/departments', tags=['Departments'])


@router.get("/all/")
async def get_all_departments(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await DepartmentsDAO.find_all()


@router.get('/get_by_id/')
async def get_department_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await DepartmentsDAO.find_one_or_none_by_id(id)
    print(result)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_status(
    response: Response,
    new_department: SNewDepartment,
    user_data: Employee = Depends(get_current_admin_user)
):
    await DepartmentsDAO.add(
        name=new_department.name,
        lead_id=new_department.lead_id
    )
    return {
        'message': 'New department was added successfully!'
    }


@router.put("/update/")
async def update_status(
    response: Response,
    update: SUpdateDepartment,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await DepartmentsDAO.update(
        filter_by={'id': update.id},
        name=update.name,
        lead_id=update.lead_id
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Отдел не обновлен. ID={update.id} не найден'
        )
    return {
        'message': f'Department(id={update.id}) was updated successfully'
    }
