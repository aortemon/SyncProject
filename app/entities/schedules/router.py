from fastapi import APIRouter, Depends, HTTPException, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.schedules.dao import SchedulesDAO
from app.entities.schedules.schemas import SNewSchedule, SUpdateSchedule

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.get("/all/")
async def get_all_schedules(user_data: Employee = Depends(require_access(ANY_USER))):
    return await SchedulesDAO.find_all()


@router.get("/get_by_id/")
async def get_schedule_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await SchedulesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_schedule(
    new_item: SNewSchedule,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await SchedulesDAO.add(**new_item.dict())
    return {"message": "New schedule was added successfully!"}


@router.put("/update/")
async def update_schedule(
    update: SUpdateSchedule,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    id = getattr(update, "id", -1)
    result = await SchedulesDAO.update(filter_by={"id": id}, **update.model_dump())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Schedule was not updated. ID={id} not found",
        )
    return {"message": f"Schedule(id={id}) was updated successfully"}
