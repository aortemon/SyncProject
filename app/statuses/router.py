from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.statuses.dao import StatusesDAO
from app.statuses.schemas import SNewStatus, SUpdateStatus
from app.employees.models import Employee
from app.employees.dependencies import get_current_admin_user


router = APIRouter(prefix='/statuses', tags=['Statuses'])


@router.get("/all/")
async def get_all_users(user_data: Employee = Depends(get_current_admin_user)):
    return await StatusesDAO.find_all()


@router.get('/get_by_id/')
async def get_status_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await StatusesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_status(
    response: Response,
    new_status: SNewStatus,
    user_data: Employee = Depends(get_current_admin_user)
):
    await StatusesDAO.add(alias=new_status.alias)
    return {
        'message': f'New status "{new_status.alias}" successfully added!'
    }


@router.put("/update/")
async def update_status(
    response: Response,
    update: SUpdateStatus,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await StatusesDAO.update(
        filter_by={'id': update.id},
        alias=update.alias
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Статус не обновлен. ID={update.id} не найден'
        )
    return {
        'message': f'Status(id={update.id}) is "{update.alias}" now'
    }
