from app.entities.common.dao import BaseDAO
from app.entities.releases.models import Release


class ReleasesDAO(BaseDAO):
    model = Release
