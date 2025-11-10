from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
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
    print(response)
    await VacationsDAO.add(**new_department.model_dump())
    return {"message": "New vacation was added successfully!"}


@router.put("/update/")
async def update_vacation(
    response: Response,
    update: SUpdateVacation,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    result = await VacationsDAO.update(
        filter_by={"id": update.id}, **update.model_dump()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department was not updated. ID={update.id} not found",
        )
    return {"message": f"Vacation(id={update.id}) was updated successfully"}
