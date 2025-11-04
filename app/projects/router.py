from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.projects.dao import ProjectDAO
from app.projects.schemas import SNewProject, SUpdateProject
from app.employees.models import Employee
from app.auth.dependencies import get_current_admin_user


router = APIRouter(prefix='/projects', tags=['Projects'])


@router.get("/all/")
async def get_all_projects(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await ProjectDAO.find_all()


@router.get('/get_by_id/')
async def get_project_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await ProjectDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_project(
    response: Response,
    new_item: SNewProject,
    user_data: Employee = Depends(get_current_admin_user)
):
    await ProjectDAO.add(
        name=new_item.name,
        description=new_item.description,
        manager_id=new_item.manager_id,
        status_id=new_item.status_id,
        release_id=new_item.release_id
    )
    return {
        'message': 'New project was added successfully!'
    }


@router.put("/update/")
async def update_project(
    response: Response,
    update: SUpdateProject,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await ProjectDAO.update(
        filter_by={'id': update.id},
        description=update.description,
        manager_id=update.manager_id,
        status_id=update.status_id,
        release_id=update.release_id
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Project was not updated. ID={update.id} not found'
        )
    return {
        'message': f'Project(id={update.id}) was updated successfully'
    }
