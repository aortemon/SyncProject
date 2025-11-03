from app.common.dao import BaseDAO
from app.releases.models import Release


class ReleasesDAO(BaseDAO):
    model = Release
