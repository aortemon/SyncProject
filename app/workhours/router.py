from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.workhours.dao import WorkHoursDAO
from app.workhours.schemas import SNewWorkhour, SUpdateWorkhour
from app.employees.models import Employee
from app.auth.dependencies import get_current_admin_user


router = APIRouter(prefix='/workhours', tags=['Work Hours'])


@router.get("/all/")
async def get_all_workours(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await WorkHoursDAO.find_all()


@router.post("/add/")
async def add_workhour(
    response: Response,
    new_workhour: SNewWorkhour,
    user_data: Employee = Depends(get_current_admin_user)
):
    await WorkHoursDAO.add(
        starttime=new_workhour.starttime,
        endtime=new_workhour.endtime,
        lunchbreak_start=new_workhour.lunchbreak_start,
        lunchbreak_end=new_workhour.lunchbreak_end
    )
    return {'message': 'New workhour successfully added'}


@router.get('/get_by_id/')
async def get_workhour_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await WorkHoursDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.put("/update/")
async def update_workhour(
    response: Response,
    update: SUpdateWorkhour,
    user_Data: Employee = Depends(get_current_admin_user)
):
    result = await WorkHoursDAO.update(
        filter_by={'id': update.id},
        starttime=update.starttime,
        endtime=update.endtime,
        lunchbreak_start=update.lunchbreak_start,
        lunchbreak_end=update.lunchbreak_end
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Worhour не обновлен. ID={update.id} не найден'
        )
    return {
        'message': f'Workhour(id={update.id}) successfully updated'
    }


# @router.post("/add/")
# async def add_status(
#     response: Response,
#     new_status: SNewStatus,
#     user_data: Employee = Depends(get_current_admin_user)
# ):
#     await StatusesDAO.add(alias=new_status.alias)
#     return {
#         'message': f'New status "{new_status.alias}" successfully added!'
#     }


# @router.put("/update/")
# async def update_status(
#     response: Response,
#     update: SUpdateStatus,
#     user_data: Employee = Depends(get_current_admin_user)
# ):
#     result = await StatusesDAO.update(
#         filter_by={'id': update.id},
#         alias=update.alias
#     )
#     if result == 0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f'Статус не обновлен. ID={update.id} не найден'
#         )
#     return {
#         'message': f'Status(id={update.id}) is "{update.alias}" now'
#     }
