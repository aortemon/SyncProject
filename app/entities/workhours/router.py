from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.workhours.dao import WorkHoursDAO
from app.entities.workhours.schemas import SNewWorkhour, SUpdateWorkhour

router = APIRouter(prefix="/workhours", tags=["Work Hours"])


@router.get("/all/")
async def get_all_workours(user_data: Employee = Depends(require_access(ANY_USER))):
    return await WorkHoursDAO.find_all()


@router.get("/get_by_id/")
async def get_workhour_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await WorkHoursDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_workhour(
    new_item: SNewWorkhour,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await WorkHoursDAO.add(**new_item.model_dump())
    return {"message": "New workhour successfully added"}


@router.put("/update/")
async def update_workhour(
    update: SUpdateWorkhour,
    user_Data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    upd_dict = update.model_dump(exclude_none=True)
    id = upd_dict["id"]
    result = await WorkHoursDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"message": f"Workhour(id={id}) successfully updated"}
