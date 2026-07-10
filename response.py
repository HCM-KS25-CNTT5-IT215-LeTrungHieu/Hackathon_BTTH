from datetime import datetime
from typing import Any, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    statusCode: int
    data: T | None = None
    message: str
    timestamp: str = datetime.now().isoformat()
    path: str
    error: Any = None
