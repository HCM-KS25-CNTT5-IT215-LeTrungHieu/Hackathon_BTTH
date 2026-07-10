from enum import StrEnum

from pydantic import BaseModel

from models import VehicleStatus


class VehicleResponse(BaseModel):
    id: str
    brand: str
    model: str
    daily_rate: float
    status: VehicleStatus


class VehicleCreate(BaseModel):
    id: str
    brand: str
    model: str
    daily_rate: float
    status: VehicleStatus


class VehicleSortBy(StrEnum):
    ID = "id"
    DAILY_RATE = "daily_rate"
    PRODUCTION_YEAR = "production_year"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
