from asyncpg import ForeignKeyViolationError, UniqueViolationError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from ._logger import logger


def exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_not_found_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            # logger.error(f"{exc}")
            logger.info(f"Redirecting to")
        elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            logger.error(f"{exc}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": f"{exc}"},
            )
        elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": f"{exc}"},
            )
        else:
            return exc

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {exc}")
        return JSONResponse(
            status_code=422,
            content={"detail": f"{exc}", "type": "db_er:sqlalchemy"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"{exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": f"{str(exc)}", "type": "http_err"},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):

        orig_exc = exc.orig

        if isinstance(orig_exc, UniqueViolationError):
            logger.error(f"UniqueViolationError: {exc}")
            return JSONResponse(
                status_code=422,
                content={
                    "detail": f"Resource already exists: {orig_exc}",
                    "type": "db_err:duplicate",
                },
            )
        elif isinstance(orig_exc, ForeignKeyViolationError):
            logger.error(f"ForeignKeyViolationError: {orig_exc}")
            return JSONResponse(
                status_code=422,
                content={
                    "detail": f"Referenced resource does not exist: {orig_exc}",
                    "type": "db_err:foreign_key",
                },
            )
        elif isinstance(orig_exc, IntegrityError) or 'IntegrityError' in str(type(orig_exc)):
            logger.error(f"ForeignKeyViolationError: {exc}")
            return JSONResponse(
                status_code=422,
                content={
                    "detail": f"Integrity error: {orig_exc}",
                    "type": "db_err:foreign_key",
                },
            )

        logger.error(f"Unhandled database integrity error: {type(exc.orig)}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Data integrity error {orig_exc}",
                "type": "db_err:integrity",
            },
        )

    return app
