# ruff: noqa: F401

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import get_db_url
from app.departments.models import Department
from app.employeedepartments.models import EmployeeDepartment
from app.employees.models import Employee
from app.files.models import File
from app.projects.models import Project
from app.releases.models import Release
from app.roles.models import Role
from app.schedules.models import Schedule
from app.statuses.models import Status
from app.taskfiles.models import TaskFile
from app.tasks.models import Task
from app.workhours.models import WorkHour

DATABASE_URL = get_db_url()


# Creates async connection to postgsql databse using asyncpg driver
engine = create_async_engine(DATABASE_URL)

# Creates async sessions Fabric for created engine
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
