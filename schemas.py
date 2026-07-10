from pydantic import BaseModel


class VehicleResponse(BaseModel):
    id: str
    brand: str
    model: str
