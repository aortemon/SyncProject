from app.entities.common.dao import BaseDAO
from app.entities.vacations.models import Vacation


class VacationsDAO(BaseDAO):
    model = Vacation
