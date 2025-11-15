from fastapi import APIRouter, Depends


from app.entities.auth.auth import get_password_hash
from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.common.exc import NotFoundError, InvalidRequest
from app.entities.employeedepartments.dao import EmployeeDepartmentsDAO
from app.entities.employees.dao import EmployeesDAO
from app.entities.employees.models import Employee
from app.entities.employees.schemas import SUpdateEmployee
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
async def update_project(
    update: SUpdateEmployee,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
):
    async with async_session_maker() as session:
        async with session.begin():
            upd_dict = update.model_dump()
            upd_dict = {k: v for k, v in upd_dict.items() if v is not None}
            
            if 'id' not in upd_dict:
                raise InvalidRequest(detail="request body should contain 'id' argument")
            if len(upd_dict) < 2:
                raise InvalidRequest(detail="nothing to update, not enoguh arguments")
            
            if "password" in upd_dict:
                upd_dict["password"] = get_password_hash(upd_dict["password"])
            departments_list = None
            if "departments" in upd_dict:
                departments_list = upd_dict.pop("departments")
            id = getattr(update, 'id', -1)
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
