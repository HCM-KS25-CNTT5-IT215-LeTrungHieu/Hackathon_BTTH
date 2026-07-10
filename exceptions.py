from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from response import ApiResponse


class AppException(Exception):
    def __init__(
        self, status_code: int, message: str, error: str | None = None
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.error = error


def app_exception_handler(r: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            statusCode=exc.status_code,
            message=exc.message,
            error=exc.error,
            path=r.url.path,
        ).model_dump(),
    )


def validate_exception_handler(r: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=ApiResponse(
            statusCode=status.HTTP_422_UNPROCESSABLE_CONTENT,
            message="Lỗi validate dữ liệu",
            error=exc.errors(),
            path=r.url.path,
        ).model_dump(),
    )


def internal_exception_handler(r: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi phía server",
            error=exc,
            path=r.url.path,
        ).model_dump(),
    )
