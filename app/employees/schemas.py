import re
from pydantic import EmailStr, Field, field_validator
from datetime import datetime
from app.common.schema import SchemaBase


class EmployeeBase(SchemaBase):
    lname: str = Field(
        ...,
        description="Фамилия",
        min_length=3,
        max_length=50
    )
    fname: str = Field(
        ...,
        description="Имя",
        min_length=3,
        max_length=50
    )
    mname: str = Field(
        ...,
        description="Отчество",
        min_length=3,
        max_length=50
    )
    dob: datetime = Field(
        ...,
        description="Дата рождения"
    )
    schedule_id: int = Field(
        ...,
        description="Идентификатор графика"
    )
    role_id: int = Field(
        ...,
        description="Идентификатор роли"
    )
    phone: str = Field(
        ...,
        description="Сотовый номер",
        min_length=3,
        max_length=50
    )
    email: EmailStr = Field(
        ...,
        description="Электронная почта",
        min_length=3,
        max_length=50
    )
    password: str = Field(
        ...,
        description="Пароль от 8 дол 50 символов",
        min_length=8,
        max_length=50,
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, values: str) -> str:
        if not re.match(r'^\+\d{5,15}$', values):
            raise ValueError(
                'Номер телефона должен начинаться с'
                ' "+" и содержать от 5 до 15 цифр'
            )
        return values