from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import AccessDeniedError, NotFoundError
from app.entities.employees.models import Employee
from app.entities.notifications.dao import NotificationsDAO
from app.entities.notifications.schemas import SNewNotification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/my/")
async def get_all_my_notifications(
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    return await NotificationsDAO.find_all(reciever_id=user_data.id)


@router.get("/read/")
async def mark_as_read(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await NotificationsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    if user_data.id != getattr(result, "reciever_id", -1):
        raise AccessDeniedError()
    await NotificationsDAO.update(filter_by={"id": id}, is_read=True)
    return {"msg": "Successfully marked as read!"}


@router.get("/get_by_id/")
async def get_notigication_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await NotificationsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_notification(
    new_notification: SNewNotification,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await NotificationsDAO.add(**new_notification.model_dump())
    return {"msg": "Successfully added!"}


@router.delete("/remove/")
async def remove_notification(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await NotificationsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    if user_data.id != getattr(result, "reciever_id", -1):
        raise AccessDeniedError()
    await NotificationsDAO.delete(id=id)
    return {"msg": "Successfully removed!"}
