from pydantic import BaseModel, EmailStr, Field

from app.entities.employees.schemas import EmployeeBase


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description='Электронная почта')
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description='Пароль'
    )


class SEmployeeRegister(EmployeeBase):
    ...