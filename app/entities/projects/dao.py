from app.entities.common.dao import BaseDAO
from app.entities.projects.models import Project


class ProjectDAO(BaseDAO):
    model = Project
