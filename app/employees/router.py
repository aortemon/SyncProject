from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.employees.dao import EmployeesDAO
from app.employees.schemas import SUpdateEmployee
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER


router = APIRouter(prefix='/employees', tags=['Employees'])


@router.get("/all/")
async def get_all_users(
    user_data: Employee = Depends(require_access(ANY_USER))
):
    return await EmployeesDAO.find_all()


@router.get('/get_by_id/')
async def get_user_by_id(
    id: int,
    user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await EmployeesDAO.find_one_or_none_by_id(id)
    print(result)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.put("/update/")
async def update_project(
    response: Response,
    update: SUpdateEmployee,
    user_data: Employee = Depends(
        require_access([UserRole.ADMIN])
    )
):
    result = await EmployeesDAO.update(
        filter_by={'id': update.id},
        **update.dict()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Project was not updated. ID={update.id} not found'
        )
    return {
        'message': f'Project(id={update.id}) was updated successfully'
    }

