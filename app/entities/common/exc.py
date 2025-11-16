from typing import Any

from fastapi import HTTPException, status


class BaseException(HTTPException):

    def __str__(self):
        return f"{self.status_code}: {self.detail}"


class DuplicateError(BaseException):
    def __init__(self, field: str, value: Any):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Entity with {field} = {value} already exists",
        )


class UnauthorizedError(BaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization needed"
        )


class AccessDeniedError(BaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied due to unsufficient credentials",
        )


class NotFoundError(BaseException):
    def __init__(self, field: str, value: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource ({field} = {value}) not found",
        )


class InvalidRequest(BaseException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Incorrect request: {detail}",
        )
