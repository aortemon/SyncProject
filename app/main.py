import logging

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.entities.admin.router import router as router_admin
from app.entities.auth.router import router as router_auth
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

logger = logging.getLogger(__name__)
app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_not_found_handler(request: Request, exc: StarletteHTTPException):
    logging.error(f"Not found error: {exc}")
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return RedirectResponse(url="/notfound")
    return exc


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logging.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"{exc}", "type": "db_er:sqlalchemy"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": f"{str(exc)}", "type": "http_err"},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logging.error(f"Database error: {exc}")

    orig_exc = exc.orig

    if isinstance(orig_exc, UniqueViolationError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Resource already exists", "type": "db_err:duplicate"},
        )
    elif isinstance(orig_exc, ForeignKeyViolationError):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Referenced resource does not exist",
                "type": "db_err:foreign_key",
            },
        )

    return JSONResponse(
        status_code=500,
        content={"detail": "Data integrity error", "type": "db_err:integrity"},
    )


@app.get("/")
def homepage():
    return {"message": "<h1>Приветики</h1>"}


@app.get("/notfound")
def notfound():
    return {"message": "Not Found here"}


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
