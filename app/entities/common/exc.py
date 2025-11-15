from typing import Any

from fastapi import HTTPException, status


class DuplicateError(HTTPException):
    def __init__(self, field: str, value: Any):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Entity with {field} = {value} already exists",
        )


class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization needed"
        )


class AccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied due to unsufficient credentials",
        )


class NotFoundError(HTTPException):
    def __init__(self, field: str, value: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource ({field} = {value}) not found",
        )


class InvalidRequest(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Incorrect request: {detail}",
        )
