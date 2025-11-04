from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.workhours.dao import WorkHoursDAO
from app.workhours.schemas import SNewWorkhour, SUpdateWorkhour
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER


router = APIRouter(prefix='/workhours', tags=['Work Hours'])


@router.get("/all/")
async def get_all_workours(
    user_data: Employee = Depends(require_access(ANY_USER))
):
    return await WorkHoursDAO.find_all()


@router.get('/get_by_id/')
async def get_workhour_by_id(
    id: int,
    user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await WorkHoursDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_workhour(
    response: Response,
    new_item: SNewWorkhour,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    await WorkHoursDAO.add(
        **new_item.dict()
    )
    return {'message': 'New workhour successfully added'}


@router.put("/update/")
async def update_workhour(
    response: Response,
    update: SUpdateWorkhour,
    user_Data: Employee = Depends(require_access([UserRole.ADMIN]))
):
    result = await WorkHoursDAO.update(
        filter_by={'id': update.id},
        **update.dict()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Worhour was not upodate. ID={update.id} not found'
        )
    return {
        'message': f'Workhour(id={update.id}) successfully updated'
    }
