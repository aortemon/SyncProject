from functools import wraps
from typing import Callable, ParamSpec, Type, TypeVar

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

from database.session import async_session_maker

# DAO is Data Access Object

T = TypeVar("T", bound=DeclarativeBase)

P = ParamSpec("P")
R = TypeVar("R")


def with_session_begin(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        async with async_session_maker() as session:
            async with session.begin():
                result = await func(cls, session, *args, **kwargs)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result

    return wrapper


def with_session(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        async with async_session_maker() as session:
            return await func(cls, session, *args, **kwargs)

    return wrapper


class BaseDAO:
    model: Type[T] = None  # type: ignore

    # ========== FINDs ==========

    @classmethod
    @with_session
    async def find_one_or_none_by_id(cls, session, data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @with_session
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @with_session
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    # ========== ADDs ==========

    @classmethod
    async def _add_impl(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)
        session.add(new_instance)
        return new_instance

    @classmethod
    @with_session_begin
    async def add(cls, session: AsyncSession, **values):
        result = await cls._add_impl(session, **values)
        return result

    @classmethod
    async def add_with_outer_session(cls, session: AsyncSession, **values):
        return await cls._add_impl(session, **values)

    # ========== ADD MANY ==========

    @classmethod
    async def _add_many_impl(cls, session: AsyncSession, instances: list[dict]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        return new_instances

    @classmethod
    @with_session_begin
    async def add_many(cls, session: AsyncSession, instances: list[dict]):
        return await cls._add_many_impl(session, instances)

    @classmethod
    async def add_many_with_outer_session(
        cls, session: AsyncSession, instances: list[dict]
    ):
        return await cls._add_many_impl(session, instances)

    # ========== UPDATEs ==========

    @classmethod
    async def _update_impl(cls, session, filter_by, **values):
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        return getattr(result, "rowcount", -1)

    @classmethod
    @with_session_begin
    async def update(cls, session, filter_by, **values):
        return await cls._update_impl(session, filter_by, **values)

    @classmethod
    async def update_with_outer_session(cls, session, filter_by, **values):
        print(filter_by, values)
        return await cls._update_impl(session, filter_by, **values)

    # ========== DELETE ==========

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if delete_all is False:
            if not filter_by:
                raise ValueError(
                    "Необходимо указать хотя бы один параметр для удаления."
                )
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return getattr(result, "rowcount", -1)
