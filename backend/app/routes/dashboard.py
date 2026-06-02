from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.schemas import AnalyticsSnapshotResponse, DetectionResponse, AlertResponse
from app.analytics import compute_aggregates

router = APIRouter()


@router.get("/analytics", response_model=List[AnalyticsSnapshotResponse])
def get_analytics(limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_analytics(db, limit=limit)


@router.get("/detections", response_model=List[DetectionResponse])
def get_detections(limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_recent_detections(db, limit=limit)


@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_alerts(db, limit=limit)


@router.get("/summary")
def get_summary(window_minutes: int = 5):
    return compute_aggregates(window_minutes)
