from app.entities.common.dao import BaseDAO
from app.entities.meetings.models import Meeting


class MeetingsDAO(BaseDAO):
    model = Meeting
