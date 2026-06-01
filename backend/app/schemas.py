from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    service: str

class StatusResponse(BaseModel):
    uptime: str
    active_sessions: int
    alerts: int

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = 'operator'

class UserResponse(UserCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SessionCreate(BaseModel):
    user_id: Optional[int]
    status: Optional[str] = 'active'

class SessionResponse(SessionCreate):
    id: int
    started_at: datetime
    ended_at: Optional[datetime]

    class Config:
        orm_mode = True

class DetectionCreate(BaseModel):
    session_id: int
    event_type: str
    score: Optional[float] = None
    metadata: Optional[str] = None

class DetectionResponse(DetectionCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AlertCreate(BaseModel):
    session_id: int
    level: str
    message: str

class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AnalyticsSnapshotCreate(BaseModel):
    session_id: Optional[int]
    metric: str
    value: float

class AnalyticsSnapshotResponse(AnalyticsSnapshotCreate):
    id: int
    collected_at: datetime

    class Config:
        orm_mode = True

class ReportCreate(BaseModel):
    name: str
    type: str
    file_path: str

class ReportResponse(ReportCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
