from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    plate_number: str
    connector_types: List[str]

@router.get("/", response_model=List[VehicleBase])
async def get_vehicles():
    return [
        {
            "make": "BYD",
            "model": "Atto 3",
            "year": 2023,
            "plate_number": "BA-PA-1234",
            "connector_types": ["CCS2"]
        }
    ]

@router.post("/")
async def add_vehicle(vehicle: VehicleBase):
    return {"message": "Vehicle added successfully"}
