from app.common.dao import BaseDAO
from app.files.models import File


class FilesDAO(BaseDAO):
    model = File
