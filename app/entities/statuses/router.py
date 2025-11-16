from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.statuses.dao import StatusesDAO
from app.entities.statuses.schemas import SNewStatus, SUpdateStatus

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.get("/all/")
async def get_all_statuses(user_data: Employee = Depends(require_access(ANY_USER))):
    return await StatusesDAO.find_all()


@router.get("/get_by_id/")
async def get_status_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await StatusesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_status(
    new_item: SNewStatus,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await StatusesDAO.add(**new_item.model_dump())
    return {"message": f'New status "{new_item.alias}" successfully added!'}


@router.put("/update/")
async def update_status(
    update: SUpdateStatus,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    upd_dict = update.model_dump(exclude_none=True)
    id = upd_dict["id"]
    result = await StatusesDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {
        "message": f'Status(id={id}) is "{getattr(update, "alias", "Unknown")}" now'
    }
