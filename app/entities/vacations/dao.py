from datetime import date

from sqlalchemy import Delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError

from app.entities.common.dao import BaseDAO
from app.entities.vacations.models import Vacation
from database.session import async_session_maker


class VacationsDAO(BaseDAO):
    model = Vacation

    @classmethod
    async def delete_past(cls):
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter(cls.model.end_day < date.today())  # type: ignore
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return getattr(result, "rowcount", -1)
