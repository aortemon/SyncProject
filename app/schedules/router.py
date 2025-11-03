from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.schedules.dao import SchedulesDAO
from app.schedules.schemas import SNewSchedule, SUpdateSchedule
from app.employees.models import Employee
from app.employees.dependencies import get_current_admin_user


router = APIRouter(prefix='/schedules', tags=['Schedules'])


@router.get("/all/")
async def get_all_schedules(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await SchedulesDAO.find_all()


@router.post("/add/")
async def add_status(
    response: Response,
    new_schedule: SNewSchedule,
    user_data: Employee = Depends(get_current_admin_user)
):
    await SchedulesDAO.add(
        sun_id=new_schedule.sun_id,
        mon_id=new_schedule.mon_id,
        tue_id=new_schedule.tue_id,
        wed_id=new_schedule.wed_id,
        thu_id=new_schedule.thu_id,
        fri_id=new_schedule.fri_id,
        sat_id=new_schedule.sat_id
    )
    return {
        'message': 'New schedule was added successfully!'
    }


@router.put("/update/")
async def update_status(
    response: Response,
    update: SUpdateSchedule,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await SchedulesDAO.update(
        filter_by={'id': update.id},
        sun_id=update.sun_id,
        mon_id=update.mon_id,
        tue_id=update.tue_id,
        wed_id=update.wed_id,
        thu_id=update.thu_id,
        fri_id=update.fri_id,
        sat_id=update.sat_id
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Расписание не обновлено. ID={update.id} не найден'
        )
    return {
        'message': f'Schedule(id={update.id}) was updated successfully'
    }
