from enum import StrEnum

from pydantic import BaseModel


class VehicleResponse(BaseModel):
    id: str
    brand: str
    model: str


class VehicleSortBy(StrEnum):
    ID = "id"
    DAILY_RATE = "daily_rate"
    PRODUCTION_YEAR = "production_year"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
