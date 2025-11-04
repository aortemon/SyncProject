from pydantic import EmailStr, Field, field_validator, PastDate
from datetime import date, timedelta
from app.common.schema import SchemaBase, Validate


class EmployeeBase(SchemaBase):
    lname: str = Field(
        ...,
        description="Фамилия",
        examples=['Пупкин'],
        min_length=3,
        max_length=50
    )
    fname: str = Field(
        ...,
        description="Имя",
        examples=['Василий'],
        min_length=3,
        max_length=50
    )
    mname: str = Field(
        ...,
        description="Отчество",
        examples=['Акакиевич'],
        min_length=3,
        max_length=50
    )
    dob: PastDate = Field(
        ...,
        description="Дата рождения YYYY-MM-DD",
        le=date.today() - timedelta(days=365*16)
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
        examples=["+79051534857"],
        min_length=12,
        max_length=12
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
        min_length=12,
        max_length=48,
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
        return Validate.phone(value)

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        return Validate.password(value)
