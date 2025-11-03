from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.releases.dao import ReleasesDAO
from app.releases.schemas import SNewRelease, SUpdateRelease
from app.employees.models import Employee
from app.auth.dependencies import get_current_admin_user


router = APIRouter(prefix='/releases', tags=['Releases'])


@router.get("/all/")
async def get_all_releases(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await ReleasesDAO.find_all()


@router.get('/get_by_id/')
async def get_release_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await ReleasesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_release(
    response: Response,
    new_item: SNewRelease,
    user_data: Employee = Depends(get_current_admin_user)
):
    await ReleasesDAO.add(
        name=new_item.name,
        version=new_item.version,
        description=new_item.description,
        status_id=new_item.status_id
    )
    return {
        'message': 'New release was added successfully!'
    }


@router.put("/update/")
async def update_release(
    response: Response,
    update: SUpdateRelease,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await ReleasesDAO.update(
        filter_by={'id': update.id},
        name=update.name,
        version=update.version,
        description=update.description,
        status_id=update.status_id
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Релиз не обновлен. ID={update.id} не найден'
        )
    return {
        'message': f'Release(id={update.id}) was updated successfully'
    }
