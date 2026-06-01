from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    service: str

class StatusResponse(BaseModel):
    uptime: str
    active_sessions: int
    alerts: int

class AlertCreate(BaseModel):
    session_id: int
    level: str
    message: str

class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
