from fastapi import Depends, FastAPI, Request, status as s
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, db_session, engine
from exceptions import (
    AppException,
    app_exception_handler,
    internal_exception_handler,
    validate_exception_handler,
)
from models import Vehicle, VehicleStatus
from response import ApiResponse
from schemas import (
    SortOrder,
    VehicleCreate,
    VehicleResponse,
    VehicleSortBy,
    VehicleUpdate,
)

SORT_COLUMNS = {
    VehicleSortBy.ID: Vehicle.id,
    VehicleSortBy.DAILY_RATE: Vehicle.daily_rate,
    VehicleSortBy.PRODUCTION_YEAR: Vehicle.production_year,
}

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_exception_handler(AppException, app_exception_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, validate_exception_handler)  # type: ignore
app.add_exception_handler(Exception, internal_exception_handler)


@app.get(
    "/vehicles",
    tags=["Vehicles"],
    response_model=ApiResponse[list[VehicleResponse]],
    status_code=s.HTTP_200_OK,
)
def get_vehicles(
    r: Request,
    brand: str | None = None,
    status: VehicleStatus | None = None,
    sort_by: VehicleSortBy = VehicleSortBy.ID,
    order: SortOrder = SortOrder.ASC,
    db: Session = Depends(db_session),
):

    stmt = select(Vehicle)
    if brand:
        stmt = stmt.where(Vehicle.brand.ilike(f"%{brand}%"))
    if status:
        stmt = stmt.where(Vehicle.status == status)

    column = SORT_COLUMNS[sort_by]
    stmt = stmt.order_by(column.desc() if order == SortOrder.DESC else column.asc())

    vehicles = db.scalars(stmt).all()

    return ApiResponse(
        statusCode=s.HTTP_200_OK,
        data=vehicles,
        message="Lấy danh sách phương tiện thành công",
        path=r.url.path,
    )


@app.get(
    "/vehicles/{vehicle_id}",
    status_code=s.HTTP_200_OK,
    response_model=ApiResponse[VehicleResponse],
    tags=["Vehicles"],
)
def get_vehicle_by_id(vehicle_id: str, r: Request, db: Session = Depends(db_session)):
    vehicle = db.get(Vehicle, vehicle_id)

    if not vehicle:
        raise AppException(
            status_code=s.HTTP_404_NOT_FOUND, message="Không tồn tại phương tiện"
        )

    return ApiResponse(
        statusCode=s.HTTP_200_OK,
        data=vehicle,
        message="Lấy dữ liệu phương tiện thành công",
        path=r.url.path,
    )


@app.post(
    "/vehicles",
    status_code=s.HTTP_201_CREATED,
    response_model=ApiResponse[VehicleResponse],
)
def create_vehicle(body: VehicleCreate, r: Request, db: Session = Depends(db_session)):
    vehicle = db.get(Vehicle, body.id)

    if vehicle:
        raise AppException(
            status_code=s.HTTP_409_CONFLICT, message="Mã phương tiện đã tồn tại"
        )

    new_vehicle = Vehicle(**body.model_dump())

    db.add(new_vehicle)

    return ApiResponse(
        statusCode=s.HTTP_201_CREATED,
        message="Tạo phương tiện thành công",
        data=new_vehicle,
        path=r.url.path,
    )


@app.put(
    "/vehicles/{vehicle_id}",
    status_code=s.HTTP_200_OK,
    response_model=ApiResponse[VehicleResponse],
)
def update_vehicle(
    vehicle_id: str, body: VehicleUpdate, r: Request, db: Session = Depends(db_session)
):
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise AppException(
            status_code=s.HTTP_404_NOT_FOUND, message="Không tìm thấy phương tiện"
        )

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)

    return ApiResponse(
        statusCode=s.HTTP_200_OK,
        message="Cập nhận phương tiện thành công",
        data=vehicle,
        path=r.url.path,
    )


@app.delete(
    "/vehicles/{vehicle_id}",
    status_code=s.HTTP_200_OK,
    response_model=ApiResponse[VehicleResponse],
)
def delete_vehicle(vehicle_id: str, r: Request, db: Session = Depends(db_session)):
    vehicle = db.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise AppException(
            status_code=s.HTTP_404_NOT_FOUND, message="Không tìm thấy phương tiện"
        )

    db.delete(vehicle)

    return ApiResponse(
        statusCode=s.HTTP_200_OK,
        message="Xoá phương tiện thành công",
        data=vehicle,
        path=r.url.path,
    )
