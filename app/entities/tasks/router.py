import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError

from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.files.dao import FilesDAO
from app.entities.files.schemas import SNewFile
from app.entities.taskfiles.dao import TaskFilesDAO
from app.entities.tasks.dao import TasksDAO
from app.entities.tasks.schemas import SNewTask, SUpdateTask
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
        raise NotFoundError(field="id", value=id)
    return result


@router.get("/my_tasks")
async def get_my_tasks(
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER]))
):
    result = await TasksDAO.find_all(creator_id=user_data.id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.get("/get_by_id/")
async def get_task_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await TasksDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_task(
    new_item: SNewTask = Depends(),
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
    files: Optional[List[UploadFile]] = File(None),
):

    async with async_session_maker() as session:
        async with session.begin():
            new_item_dict = {**new_item.model_dump(), "creator_id": user_data.id}
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
    update: SUpdateTask,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    id = getattr(update, "id", -1)
    result = await TasksDAO.update(filter_by={"id": id}, **update.model_dump())
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"message": f"Task(id={id}) was updated successfully"}
