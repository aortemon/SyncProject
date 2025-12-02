import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app._logger import logger
from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employees.models import Employee
from app.entities.files.dao import FilesDAO
from app.entities.files.schemas import SNewFile
from app.entities.taskcomments.dao import TaskCommentDAO
from app.entities.taskcomments.schemas import SAddComment
from app.entities.taskfiles.dao import TaskFilesDAO
from app.entities.tasks.dao import TasksDAO
from app.entities.tasks.schemas import SNewTask, SUpdateTask
from database.session import Sessioner

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
    async with Sessioner.session_maker() as session:
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
                    logger.info(f"Added file: {file_data.source[1:]}")
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
    return {"msg": "Successfully added!"}


@router.put("/update/")
async def update_task(
    update: SUpdateTask,
    user_data: Employee = Depends(
        require_access([UserRole.ADMIN, UserRole.MANAGER, UserRole.EXECUTOR])
    ),
):
    upd_dict = update.model_dump(exclude_none=True)
    has_start_date = "start_date" in upd_dict
    has_end_date = "end_date" in upd_dict
    id = upd_dict["id"]
    if has_start_date ^ has_end_date:
        previous = await TasksDAO.find_one_or_none_by_id(id)
        if not previous:
            raise NotFoundError(field="id", value=id)

        if "start_date" not in upd_dict or not upd_dict["start_date"]:
            upd_dict["start_date"] = previous.start_date
        if "end_date" not in upd_dict or not upd_dict["end_date"]:
            upd_dict["end_date"] = previous.end_date
        new_schema = SUpdateTask(**upd_dict)
        upd_dict = new_schema.model_dump(exclude_none=True)

        if not has_start_date:
            del upd_dict["start_date"]

        if not has_end_date:
            del upd_dict["end_date"]

    result = await TasksDAO.update(filter_by={"id": id}, **upd_dict)
    if result == 0:
        raise NotFoundError(field="id", value=id)
    return {"msg": f"Task(id={id}) was updated successfully"}


@router.delete("/delete/")
async def delete_task(
    id: int,
    user_data: Employee = Depends(require_access([UserRole.ADMIN, UserRole.MANAGER])),
):
    task = await TasksDAO.find_one_or_none_by_id(data_id=id)
    if not task:
        raise NotFoundError(field="Task with id", value=id)
    await TaskCommentDAO.delete(task_id=id)
    await TaskFilesDAO.delete(task_id=id)
    await TasksDAO.delete(id=id)
    return {"msg": "Deleted successfully"}


@router.post("/comments/add/")
async def comment_task(
    comment: SAddComment,
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    add_dict = comment.model_dump()
    add_dict["author_id"] = user_data.id
    await TaskCommentDAO.add(**add_dict)
    return {"msg": "Comment added successfully"}
