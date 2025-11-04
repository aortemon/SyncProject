from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.tasks.dao import TasksDAO
from app.tasks.schemas import SNewTask, SUpdateTask
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER


router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get("/all/")
async def get_all_tasks(
    user_data: Employee = Depends(require_access(ANY_USER))
):
    return await TasksDAO.find_all()


@router.get('/get_by_id/')
async def get_task_by_id(
    id: int,
    user_data: Employee = Depends(require_access(ANY_USER))
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
    user_data: Employee = Depends(
        require_access([UserRole.ADMIN, UserRole.MANAGER])
    )
):
    await TasksDAO.add(**new_item.dict())
    return {
        'message': 'New task was added successfully!'
    }


@router.put("/update/")
async def update_task(
    response: Response,
    update: SUpdateTask,
    user_data: Employee = Depends(
        require_access([UserRole.ADMIN, UserRole.MANAGER])
    )
):
    result = await TasksDAO.update(
        filter_by={'id': update.id},
        **update.dict()
    )
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'task was not updated. ID={update.id} not found'
        )
    return {
        'message': f'Task(id={update.id}) was updated successfully'
    }
