# from datetime import datetime
from datetime import datetime
from typing import Annotated
from sqlalchemy import ForeignKey, Integer, String, func, Time
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

# from app.employees.models import Employee
from app.config import get_db_url

DATABASE_URL = get_db_url()


# Creates async connection to postgsql databse using asyncpg driver
engine = create_async_engine(DATABASE_URL)

# Creates async sessions Fabric for created engine
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
str_unque = Annotated[str, mapped_column(String(256), unique=True)]
str256 = Annotated[str, mapped_column(String(256), nullable=False)]
workhour_fk = Annotated[
    Time, mapped_column(ForeignKey("workhours.id"), nullable=False)
]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]

empls_fk = Annotated[
    int, mapped_column(ForeignKey("employees.id"), nullable=False)
]


class Base(AsyncAttrs, DeclarativeBase):
    """Abstract class for all the models with Alembic and async support"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self):
        return str(self)


class File(Base):
    id: Mapped[int_pk]
    source: Mapped[str256]
    extension: Mapped[str256]


class TaskFile(Base):
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False, primary_key=True
    )
    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id"), nullable=False, primary_key=True
    )


class EmployeeDepartment(Base):
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"), nullable=False, primary_key=True
    )
    office: Mapped[str256]
