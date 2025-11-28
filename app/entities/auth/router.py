from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError

from app.entities.auth.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.entities.auth.dependencies import ANY_USER, UserRole, require_access
from app.entities.auth.models import Token
from app.entities.auth.schemas import SEmployeeRegister
from app.entities.common.exc import DuplicateError, UnauthorizedError
from app.entities.employeedepartments.dao import EmployeeDepartmentsDAO
from app.entities.employees.dao import EmployeesDAO
from app.entities.employees.models import Employee
from database.session import async_session_maker

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(
    employee_data: SEmployeeRegister,
    user_data: Employee = Depends(require_access([UserRole.ADMIN])),
) -> dict:
    users = await EmployeesDAO.find_one_or_none(email=employee_data.email)
    if users:
        raise DuplicateError(field="id", value=users.id)
    async with async_session_maker() as session:
        async with session.begin():
            user_dict = employee_data.dict()
            departments_list = user_dict.pop("departments")
            user_dict["password"] = get_password_hash(employee_data.password)
            new_user_instance = await EmployeesDAO.add_with_outer_session(
                session, **user_dict
            )
            await session.flush()
            await EmployeeDepartmentsDAO.add_many_with_outer_session(
                session,
                [
                    {
                        "department_id": x["id"],
                        "employee_id": getattr(new_user_instance, "id", -1),
                        "office": x["office"],
                    }
                    for x in departments_list
                ],
            )
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
    return {"message": "Вы успешно зарегистрированы"}


@router.post("/login/", response_model=Token)
async def auth_user(user_data: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(
        email=user_data.username, password=user_data.password
    )
    if user is None:
        raise UnauthorizedError()
    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me/")
async def get_me(user_data: Employee = Depends(require_access(ANY_USER))):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {"message": "Logged out successfully"}


@router.get("/is_token_correct/")
async def check_is_token_correct(
    user_data: Employee = Depends(require_access(ANY_USER)),
):
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "85.143.13.238:0",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )
