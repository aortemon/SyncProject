from fastapi import APIRouter, Depends

from app.entities.auth.dependencies import UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.vacations.dao import VacationsDAO
from app.entities.vacations.schemas import SNewVacation, SUpdateVacation

router = APIRouter(prefix="/vacations", tags=["Vacations"])


@router.post("/add/")
async def add_vacation(
    new_department: SNewVacation,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await VacationsDAO.add(**new_department.model_dump())
    return {"message": "New vacation was added successfully!"}


@router.put("/update/")
async def update_vacation(
    update: SUpdateVacation,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    upd_dict = update.model_dump(exclude_none=True)
    id = upd_dict["id"]
    result = await VacationsDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"message": f"Vacation(id={id}) was updated successfully"}
