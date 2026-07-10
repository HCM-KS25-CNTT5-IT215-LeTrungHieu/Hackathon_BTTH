import enum

from sqlalchemy import CheckConstraint, Enum, String, column, func, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class VehicleStatus(enum.Enum):
    AVAILABLE = "avaiable"
    RENTED = "rented"
    MAINTENANCE = "maintenance"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(7), primary_key=True)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    daily_rate: Mapped[float]
    production_year: Mapped[int]
    status: Mapped[VehicleStatus] = mapped_column(
        Enum(VehicleStatus), server_default=text("'available'")
    )

    __table_args__ = (
        CheckConstraint(func.char_length(column("brand")) >= 2),
        CheckConstraint(column("daily_rate") > 0),
        CheckConstraint(column("production_year").between(2010, 2026)),
    )
