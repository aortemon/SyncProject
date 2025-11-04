from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.auth.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from app.employees.dao import EmployeesDAO
from app.auth.schemas import SEmployeeRegister, SUserAuth
from app.employees.models import Employee
from app.auth.dependencies import require_access, UserRole, ANY_USER

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(
    employee_data: SEmployeeRegister,
    user_data: Employee = Depends(require_access([UserRole.ADMIN]))
) -> dict:
    users = await EmployeesDAO.find_one_or_none(email=employee_data.email)
    if users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = employee_data.dict()
    user_dict['password'] = get_password_hash(employee_data.password)
    await EmployeesDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы'}


@router.post('/login/')
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password
    )
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или параль'
        )
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(
        key="user_access_token",
        value=access_token,
        httponly=True
    )
    return {'access_token': access_token, 'refresh_token': None}


@router.get('/me/')
async def get_me(user_data: Employee = Depends(require_access(ANY_USER))):
    return user_data


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}
