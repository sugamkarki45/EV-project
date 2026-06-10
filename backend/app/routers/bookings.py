from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/")
async def create_booking(booking: dict):
    return {"id": "booking-123", "status": "pending_approval"}

@router.post("/{id}/start-session")
async def start_session(id: str):
    return {"status": "in_progress", "start_time": "2026-06-10T10:00:00Z"}

@router.post("/{id}/end-session")
async def end_session(id: str):
    return {"status": "completed", "end_time": "2026-06-10T11:30:00Z"}
