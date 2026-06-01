from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default='operator')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SessionRecord(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default='active')

class DetectionEvent(Base):
    __tablename__ = 'detections'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AlertRecord(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalyticsSnapshot(Base):
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=True)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())

class ReportRecord(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
