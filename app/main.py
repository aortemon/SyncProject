from fastapi import FastAPI
from app.employees.router import router as router_employees
from app.statuses.router import router as router_statuses
from app.workhours.router import router as router_workhours
from app.schedules.router import router as router_schedules
from app.departments.router import router as router_departments
from app.releases.router import router as router_releases
from app.projects.router import router as router_projects
from app.tasks.router import router as router_tasks
from app.auth.router import router as router_auth
from app.files.router import router as router_files

app = FastAPI()


@app.get('/')
def homepage():
    return {'message': '<h1>Приветики</h1>'}


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
