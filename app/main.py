from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.entities.admin.router import router as router_admin
from app.entities.auth.router import router as router_auth
from app.entities.common.exc import NotFoundError
from app.entities.departments.router import router as router_departments
from app.entities.employees.router import router as router_employees
from app.entities.files.router import router as router_files
from app.entities.meetings.router import router as router_meetings
from app.entities.notifications.router import router as router_notifications
from app.entities.projects.router import router as router_projects
from app.entities.releases.router import router as router_releases
from app.entities.schedules.router import router as router_schedules
from app.entities.statuses.router import router as router_statuses
from app.entities.tasks.router import router as router_tasks
from app.entities.vacations.router import router as router_vacations
from app.entities.workhours.router import router as router_workhours

from .exc_handlers import exception_handlers

app = FastAPI()

app = exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def homepage():
    return {"msg": "OK"}


@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )


app.include_router(router_auth)
app.include_router(router_admin)
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
app.include_router(router_vacations)
app.include_router(router_meetings)
app.include_router(router_notifications)
app.include_router(router_meetings)
app.include_router(router_notifications)


@app.api_route("/{anypath:path}", methods=["GET", "POST", "PUT", "PATCH"])
async def options_hander(anypath):
    raise NotFoundError("path", f"/{anypath}")
