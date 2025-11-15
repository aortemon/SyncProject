from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.vacations.dao import VacationsDAO
from app.entities.vacations.schemas import SNewVacation, SUpdateVacation

router = APIRouter(prefix="/vacations", tags=["Vacations"])


@router.post("/add/")
async def add_vacation(
    response: Response,
    new_department: SNewVacation,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    await VacationsDAO.add(**new_department.model_dump())
    return {"message": "New vacation was added successfully!"}


@router.put("/update/")
async def update_vacation(
    response: Response,
    update: SUpdateVacation,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    id = getattr(update, "id", -1)
    result = await VacationsDAO.update(filter_by={"id": id}, **update.model_dump())
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"message": f"Vacation(id={id}) was updated successfully"}
