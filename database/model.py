# from datetime import datetime
from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, Integer, String, Time, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column

# from app.entities.employees.models import Employee

int_pk = Annotated[int, mapped_column(Integer, primary_key=True)]
str_unque = Annotated[str, mapped_column(String(256), unique=True)]
str256 = Annotated[str, mapped_column(String(256), nullable=False)]
workhour_fk = Annotated[Time, mapped_column(ForeignKey("workhours.id"), nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]

empls_fk = Annotated[int, mapped_column(ForeignKey("employees.id"), nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    """Abstract class for all the models with Alembic and async support"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __str__(self):
        return f"{self.__class__.__name__}(id={getattr(self, 'id', None)})"

    def __repr__(self):
        return str(self)
