# pyright: reportAttributeAccessIssue=false

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.entities.auth.auth import get_password_hash
from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError
from app.entities.employeedepartments.dao import EmployeeDepartmentsDAO
from app.entities.employees.dao import EmployeesDAO
from app.entities.employees.models import Employee
from app.entities.employees.schemas import SCalendarDate, SUpdateEmployee
from app.entities.tasks.dao import TasksDAO
from database.session import async_session_maker

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/all/")
async def get_all_users(user_data: Employee = Depends(require_access(ANY_USER))):
    return await EmployeesDAO.find_all()


@router.get("/get_by_id/")
async def get_user_by_id(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
):
    result = await EmployeesDAO.find_one_or_none_by_id(id)
    if result is None:
        raise NotFoundError(field="id", value=id)

    return result


@router.put("/update/")
async def update_employee(
    update: SUpdateEmployee,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    async with async_session_maker() as session:
        async with session.begin():
            upd_dict = update.model_dump(exclude_none=True)
            id = upd_dict["id"]
            if "password" in upd_dict:
                upd_dict["password"] = get_password_hash(upd_dict["password"])
            departments_list = None
            if "departments" in upd_dict:
                departments_list = upd_dict.pop("departments")
            id = getattr(update, "id", -1)
            await EmployeesDAO.update_with_outer_session(
                session, filter_by={"id": id}, **upd_dict
            )
            await session.flush()
            if departments_list:
                await EmployeeDepartmentsDAO.delete(employee_id=id)
                await session.flush()
                await EmployeeDepartmentsDAO.add_many_with_outer_session(
                    session,
                    [
                        {
                            "department_id": x["id"],
                            "employee_id": id,
                            "office": x["office"],
                        }
                        for x in departments_list
                    ],
                )
            try:
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    return {"message": f"Project(id={id}) was updated successfully"}


async def get_calendar_date(user_id: int, day: date) -> SCalendarDate:
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    user_data = await EmployeesDAO.find_one_or_none_by_id(data_id=user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User set in token not found",
        )
    meetings = [
        x.meeting for x in user_data.employee_meetings if x.meeting.date.date() == day
    ]
    vacations = [x for x in user_data.vacations if x.start_day < day < x.end_day]
    workhours = getattr(user_data.schedule, weekdays[day.weekday()], -1)
    tasks = await TasksDAO.find_all(executor_id=user_id)
    tasks = [x for x in tasks if x.start_date.date() <= day <= x.end_date.date()]

    response = SCalendarDate(
        day=day,
        is_vacation=len(vacations) != 0,
        is_weekend=workhours.starttime == workhours.endtime,
        task_deadlines=[
            (x.name, f"/tasks/get_by_id/{x.id}")
            for x in tasks
            if x.end_date.date() == day
        ],
        timesheet=sorted(
            [
                (workhours.starttime.strftime("%H:%M"), "Начало рабочего дня", ""),
                (workhours.endtime.strftime("%H:%M"), "Конец рабочего дня", ""),
                (workhours.lunchbreak_start.strftime("%H:%M"), "Начало обеда", ""),
                (workhours.lunchbreak_end.strftime("%H:%M"), "Конец обеда", ""),
                *[
                    (x.date.strftime("%H:%M"), f"Собрание {x.name}", "")
                    for x in meetings
                ],
                *[
                    (
                        x.start_date.time().strftime("%H:%M"),
                        f'Старт задачи "{x.name}"',
                        f"/get_task_by_id/{x.id}",
                    )
                    for x in tasks
                    if x.start_date.date() == day
                ],
                *[
                    (
                        x.end_date.time().strftime("%H:%M"),
                        f'Дедлайн задачи "{x.name}"',
                        f"/get_task_by_id/{x.id}",
                    )
                    for x in tasks
                    if x.end_date.date() == day
                ],
            ]
        ),
        active_tasks=[(x.name, f"/get_task_by_id/{x.id}") for x in tasks],
    )  # type: ignore

    return response


@router.get("/calendar/mine/today/")
async def get_my_schedule_for_today(
    user_data: Employee = Depends(require_access(ANY_USER)),
) -> SCalendarDate:
    return await get_calendar_date(user_data.id, datetime.today().date())


@router.get("/calendar/mine/")
async def get_my_schedule_exact_day(
    date: date, user_data: Employee = Depends(require_access(ANY_USER))
) -> SCalendarDate:
    return await get_calendar_date(user_data.id, date)


@router.get("/calendar/get_todays_by_user_id")
async def get_someones_schedule_for_today(
    id: int, user_data: Employee = Depends(require_access(ANY_USER))
) -> SCalendarDate:
    return await get_calendar_date(id, datetime.today().date())


@router.get("/calendar/get_by_user_id_and_date")
async def get_someones_schedule_by_id_and_date(
    id: int, date: date, user_data: Employee = Depends(require_access(ANY_USER))
) -> SCalendarDate:
    return await get_calendar_date(id, date)
