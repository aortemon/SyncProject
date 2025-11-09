import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.exc import SQLAlchemyError

from app.auth.dependencies import ANY_USER, UserRole, require_access
from app.employees.models import Employee
from app.files.dao import FilesDAO
from app.files.schemas import SNewFile
from app.taskfiles.dao import TaskFilesDAO
from app.tasks.dao import TasksDAO
from app.tasks.schemas import SNewTask, SUpdateTask
from database.session import async_session_maker

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/all/")
async def get_all_tasks(user_data: Employee = Depends(require_access(ANY_USER))):
    return await TasksDAO.find_all()


@router.get("/my_drafts")
async def get_my_drafts(
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER]))
):
    result = await TasksDAO.find_all(creator_id=user_data.id, executor_id=None)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )
    return result


@router.get("/get_by_id/")
async def get_task_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await TasksDAO.find_one_or_none_by_id(id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ID = {id} not found",
        )
    return result


@router.post("/add/")
async def add_task(
    response: Response,
    new_item: SNewTask = Depends(),
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
    files: Optional[List[UploadFile]] = File(None),
):

    async with async_session_maker() as session:
        async with session.begin():
            new_item_dict = {**new_item.model_dump(), 'creator_id': user_data.id}
            task_insert_result = await TasksDAO.add(**new_item_dict)
            if files:
                for file in files:
                    file_data = SNewFile(filename=file.filename, content_type=file.content_type)  # type: ignore
                    file_insert_result = await FilesDAO.add_with_outer_session(
                        session,
                        name=file_data.filename,
                        source=file_data.source,
                        extension=file_data.extension,
                    )
                    await session.flush()
                    if not file_insert_result:
                        raise HTTPException(
                            status_code=500, detail="Somnething went wrong"
                        )
                    dst = (
                        Path.home()
                        / "SyncProject"
                        / "user_files"
                        / file_data.source[1:]
                    )
                    with open(dst, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    await TaskFilesDAO.add_with_outer_session(
                        session,
                        task_id=task_insert_result.id,  # type: ignore
                        file_id=file_insert_result.id,  # type: ignore
                    )
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
    return {"message": "New task was added successfully!"}


@router.put("/update/")
async def update_task(
    response: Response,
    update: SUpdateTask,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    
    result = await TasksDAO.update(filter_by={"id": update.id}, **update.dict())
    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"task was not updated. ID={update.id} not found",
        )
    return {"message": f"Task(id={update.id}) was updated successfully"}
