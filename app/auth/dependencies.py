from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import get_auth_data
from app.employees.dao import EmployeesDAO
from app.employees.models import Employee


def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Auth-токен не найден'
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token,
            auth_data['secret_key'],
            algorithms=[auth_data['algorithm']]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не валиден'
        )
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Срок жизни токена истек'
        )
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='ID пользователя не найден'
        )
    user = await EmployeesDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден'
        )
    return user


async def get_current_admin_user(
    current_user: Employee = Depends(get_current_user)
):
    if current_user.role.description == 'admin':
        return current_user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недостаточно прав!'
        )
