from enum import StrEnum

from pydantic import BaseModel, Field

from models import VehicleStatus


class VehicleResponse(BaseModel):
    id: str
    brand: str
    model: str
    daily_rate: float
    production_year: int
    status: VehicleStatus


class VehicleCreate(BaseModel):
    id: str = Field(min_length=7, max_length=7)
    brand: str = Field(min_length=2, max_length=50)
    model: str = Field(max_length=50)
    daily_rate: float = Field(gt=0)
    production_year: int = Field(ge=2010, le=2026)
    status: VehicleStatus


class VehicleUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=2, max_length=50)
    model: str | None = Field(default=None, max_length=50)
    daily_rate: float | None = Field(default=None, gt=0)
    production_year: int | None = Field(default=None, ge=2010, le=2026)
    status: VehicleStatus | None = Field(default=None)


class VehicleSortBy(StrEnum):
    ID = "id"
    DAILY_RATE = "daily_rate"
    PRODUCTION_YEAR = "production_year"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
