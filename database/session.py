# ruff: noqa: F401

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import get_db_url
from app.entities.departments.models import Department
from app.entities.employeedepartments.models import EmployeeDepartment
from app.entities.employees.models import Employee
from app.entities.files.models import File
from app.entities.meetings.models import Meeting
from app.entities.projects.models import Project
from app.entities.releases.models import Release
from app.entities.roles.models import Role
from app.entities.schedules.models import Schedule
from app.entities.statuses.models import Status
from app.entities.taskfiles.models import TaskFile
from app.entities.tasks.models import Task
from app.entities.vacations.models import Vacation
from app.entities.workhours.models import WorkHour

DATABASE_URL = get_db_url()


# Creates async connection to postgsql databse using asyncpg driver
engine = create_async_engine(DATABASE_URL)

# Creates async sessions Fabric for created engine
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
