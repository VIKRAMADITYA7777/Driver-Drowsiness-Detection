from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.reports import generate_csv_report

router = APIRouter()


class ReportRequest(BaseModel):
    session_id: Optional[int] = None
    window_minutes: int = 60


@router.post("/generate")
def generate_report(req: ReportRequest):
    path = generate_csv_report(session_id=req.session_id, window_minutes=req.window_minutes)
    return {"path": str(path)}
