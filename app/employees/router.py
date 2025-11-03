from fastapi import APIRouter, HTTPException, status, Depends
from app.employees.dao import EmployeesDAO
from app.employees.models import Employee
from app.auth.dependencies import get_current_admin_user


router = APIRouter(prefix='/employees', tags=['Employees'])


@router.get("/all/")
async def get_all_users(user_data: Employee = Depends(get_current_admin_user)):
    return await EmployeesDAO.find_all()


@router.get('/get_by_id/')
async def get_user_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await EmployeesDAO.find_one_or_none_by_id(id)
    print(result)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result
