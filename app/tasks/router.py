from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.tasks.dao import TasksDAO
from app.tasks.schemas import SNewTask, SUpdateTask
from app.employees.models import Employee
from app.employees.dependencies import get_current_admin_user


router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get("/all/")
async def get_all_tasks(
    user_data: Employee = Depends(get_current_admin_user)
):
    return await TasksDAO.find_all()


@router.get('/get_by_id/')
async def get_department_by_id(
    id: int,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await TasksDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found"
        )
    return result


@router.post("/add/")
async def add_task(
    response: Response,
    new_item: SNewTask,
    user_data: Employee = Depends(get_current_admin_user)
):
    await TasksDAO.add(
        name=new_item.name,
        description=new_item.description,
        creator_id=new_item.creator_id,
        executor_id=new_item.executor_id,
        status_id=new_item.status_id,
        project_id=new_item.project_id,
        start_date=new_item.start_date,
        end_date=new_item.end_date
    )
    return {
        'message': 'New task was added successfully!'
    }


@router.put("/update/")
async def update_task(
    response: Response,
    update: SUpdateTask,
    user_data: Employee = Depends(get_current_admin_user)
):
    result = await TasksDAO.update(
        filter_by={'id': update.id},
        name=update.name,
        description=update.description,
        creator_id=update.creator_id,
        executor_id=update.executor_id,
        status_id=update.status_id,
        project_id=update.project_id,
        start_date=update.start_date,
        end_date=update.end_date
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'задача не обновлена. ID={update.id} не найден'
        )
    return {
        'message': f'Task(id={update.id}) was updated successfully'
    }
