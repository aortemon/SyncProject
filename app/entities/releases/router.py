from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.releases.dao import ReleasesDAO
from app.entities.releases.schemas import SNewRelease, SUpdateRelease

router = APIRouter(prefix="/releases", tags=["Releases"])


@router.get("/all/")
async def get_all_releases(user_data: Employee = Depends(require_access(ANY_USER))):
    return await ReleasesDAO.find_all()


@router.get("/get_by_id/")
async def get_release_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await ReleasesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field='id', value=id)
    return result


@router.post("/add/")
async def add_release(
    response: Response,
    new_item: SNewRelease,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    await ReleasesDAO.add(**new_item.dict())
    return {"message": "New release was added successfully!"}


@router.put("/update/")
async def update_release(
    response: Response,
    update: SUpdateRelease,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    id = getattr(update, 'id', -1)
    result = await ReleasesDAO.update(filter_by={"id": id}, **update.model_dump())
    if result == 0:
        raise NotFoundError(field='id', value=id)
    return {"message": f"Release(id={id}) was updated successfully"}
