from fastapi import APIRouter
from app.schemas import HealthResponse

router = APIRouter()

@router.get("/status", response_model=HealthResponse)
async def get_health_status():
    return {"status": "ok", "service": "driver-drowsiness-backend"}
