from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.entities.auth.dependencies import ANY_USER, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employeemeetings.dao import EmployeeMeetingsDAO
from app.entities.employees.models import Employee
from app.entities.meetings.dao import MeetingsDAO
from app.entities.meetings.schemas import SNewMeeting, SUpdateMeeting
from database.session import Sessioner

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("/all/")
async def get_all_meetings(user_data: Employee = Depends(require_access(ANY_USER))):
    return await MeetingsDAO.find_all()


@router.get("/get_by_id/")
async def get_meeting_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await MeetingsDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)
    return result


@router.post("/add/")
async def add_meeting(
    new_meeting: SNewMeeting,
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    async with Sessioner.session_maker() as session:
        async with session.begin():
            meeting_data = new_meeting.model_dump()
            meeting_data["creator_id"] = user_data.id
            employees = meeting_data.pop("employees")
            meeting_result = await MeetingsDAO.add_with_outer_session(
                session, **meeting_data
            )
            await session.flush()
            if meeting_result:
                for empl in employees:
                    await EmployeeMeetingsDAO.add_with_outer_session(
                        session, meeting_id=meeting_result.id, employee_id=empl  # type: ignore
                    )
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    return {"msg": "Successfully added!"}


@router.put("/update/")
async def update_meeting(
    update: SUpdateMeeting,
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    meeting_data = update.model_dump(exclude_none=True)
    employees = []
    if "employees" in meeting_data:
        employees = meeting_data.pop("employees")
        print("??????? ", employees)
        if not isinstance(employees, list):
            raise HTTPException(status_code=422, detail="Something went wrong")

    async with Sessioner.session_maker() as session:
        async with session.begin():
            meeting_result = await MeetingsDAO.update_with_outer_session(
                session, filter_by={"id": meeting_data["id"]}, **meeting_data
            )
            await session.flush()
            res = await EmployeeMeetingsDAO.delete(
                delete_all=True, meeting_id=meeting_data["id"]
            )
            await session.flush()
            if meeting_result:
                for empl in employees:
                    res = await EmployeeMeetingsDAO.add_with_outer_session(
                        session, meeting_id=meeting_data["id"], employee_id=empl
                    )
                    if not res:
                        raise HTTPException(
                            status_code=422, detail="Something went wrong"
                        )
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    return {"msg": "Successfully added!"}
