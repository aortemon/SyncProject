from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.statuses.dao import StatusesDAO
from app.statuses.schemas import SNewStatus, SUpdateStatus
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER


router = APIRouter(prefix='/statuses', tags=['Statuses'])


@router.get("/all/")
async def get_all_statuses(
    user_data: Employee = Depends(require_access(ANY_USER))
):
    return await StatusesDAO.find_all()


@router.get('/get_by_id/')
async def get_status_by_id(
    id: int,
    user_data: Employee = Depends(require_access(ANY_USER))
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
    new_item: SNewStatus,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    await StatusesDAO.add(**new_item.dict())
    return {
        'message': f'New status "{new_item.alias}" successfully added!'
    }


@router.put("/update/")
async def update_status(
    response: Response,
    update: SUpdateStatus,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    result = await StatusesDAO.update(
        filter_by={'id': update.id},
        **update.dict()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Status was not updated. ID={update.id} not found'
        )
    return {
        'message': f'Status(id={update.id}) is "{update.alias}" now'
    }
