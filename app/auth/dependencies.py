from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import get_auth_data
from app.employees.dao import EmployeesDAO
from app.employees.models import Employee
from enum import Enum
from typing import List


class UserRole(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    EXECUTOR = 'executor'


ANY_USER = [UserRole.ADMIN, UserRole.MANAGER, UserRole.EXECUTOR]


def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Auth-token not found'
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        # payload is dict containing sub - id of user
        # and exp - date of expiration
        payload = jwt.decode(
            token,
            auth_data['secret_key'],
            algorithms=[auth_data['algorithm']]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is expired'
        )
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No user_id found in token'
        )
    user = await EmployeesDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User set in token not found'
        )
    return user


async def get_current_admin_user(
    current_user: Employee = Depends(get_current_user)
):
    if current_user.role.description == 'admin':
        return current_user
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permission denied'
        )


async def check_user_permission(
    current_user: Employee = Depends(get_current_user),
    required_access_level: List[UserRole] = [UserRole.ADMIN]
) -> Employee:
    if current_user.role.description in required_access_level:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Access denied due to unsufficient privileges'
    )


# Fabric of dependencies for all the required access levels
def require_access(required_access_level: List[UserRole]):
    async def dependency(
        current_user: Employee = Depends(get_current_user)
    ):
        return await check_user_permission(current_user, required_access_level)
    return dependency
