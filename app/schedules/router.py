from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.schedules.dao import SchedulesDAO
from app.schedules.schemas import SNewSchedule, SUpdateSchedule
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER


router = APIRouter(prefix='/schedules', tags=['Schedules'])


@router.get("/all/")
async def get_all_schedules(
    user_data: Employee = Depends(require_access(ANY_USER))
):
    return await SchedulesDAO.find_all()


@router.get('/get_by_id/')
async def get_schedule_by_id(
    id: int,
    user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await SchedulesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_schedule(
    response: Response,
    new_item: SNewSchedule,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    await SchedulesDAO.add(**new_item.dict())
    return {
        'message': 'New schedule was added successfully!'
    }


@router.put("/update/")
async def update_schedule(
    response: Response,
    update: SUpdateSchedule,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    result = await SchedulesDAO.update(
        filter_by={'id': update.id},
        **update.dict()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Schedule was not updated. ID={update.id} not found'
        )
    return {
        'message': f'Schedule(id={update.id}) was updated successfully'
    }
