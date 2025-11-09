from app.entities.common.dao import BaseDAO
from app.entities.files.models import File


class FilesDAO(BaseDAO):
    model = File
