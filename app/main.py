from fastapi import FastAPI

from app.entities.auth.router import router as router_auth
from app.entities.departments.router import router as router_departments
from app.entities.employees.router import router as router_employees
from app.entities.files.router import router as router_files
from app.entities.projects.router import router as router_projects
from app.entities.releases.router import router as router_releases
from app.entities.schedules.router import router as router_schedules
from app.entities.statuses.router import router as router_statuses
from app.entities.tasks.router import router as router_tasks
from app.entities.workhours.router import router as router_workhours

app = FastAPI()


@app.get("/")
def homepage():
    return {"message": "<h1>Приветики</h1>"}


app.include_router(router_auth)
app.include_router(router_employees)
app.include_router(router_statuses)
app.include_router(router_workhours)
app.include_router(router_schedules)
app.include_router(router_departments)
app.include_router(router_releases)
app.include_router(router_projects)
app.include_router(router_tasks)
app.include_router(router_files)
app.include_router(router_files)
app.include_router(router_files)
