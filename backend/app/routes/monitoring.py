from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import StatusResponse, AlertCreate, AlertResponse
from app.database import get_db
from app import crud

router = APIRouter()

@router.get("/status", response_model=StatusResponse)
async def get_system_status(db: Session = Depends(get_db)):
    alerts = len(crud.get_alerts(db, limit=10))
    return {
        "uptime": "00:02:34",
        "active_sessions": 2,
        "alerts": alerts
    }

@router.post("/alerts", response_model=AlertResponse)
async def post_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    return crud.create_alert(db, alert_in)
