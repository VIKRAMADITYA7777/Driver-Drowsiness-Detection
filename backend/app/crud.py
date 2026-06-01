from sqlalchemy.orm import Session
from app import models, schemas


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        name=user_in.name,
        email=user_in.email,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).get(user_id)


def create_session(db: Session, session_in: schemas.SessionCreate) -> models.SessionRecord:
    session = models.SessionRecord(
        user_id=session_in.user_id,
        status=session_in.status
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_session_status(db: Session, session_id: int, status: str) -> models.SessionRecord | None:
    session = db.query(models.SessionRecord).get(session_id)
    if session:
        session.status = status
        db.commit()
        db.refresh(session)
    return session


def create_detection(db: Session, detection_in: schemas.DetectionCreate) -> models.DetectionEvent:
    detection = models.DetectionEvent(
        session_id=detection_in.session_id,
        event_type=detection_in.event_type,
        score=detection_in.score,
        metadata=detection_in.metadata
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


def get_recent_detections(db: Session, limit: int = 25):
    return db.query(models.DetectionEvent).order_by(models.DetectionEvent.created_at.desc()).limit(limit).all()


def create_alert(db: Session, alert_in: schemas.AlertCreate) -> models.AlertRecord:
    alert = models.AlertRecord(
        session_id=alert_in.session_id,
        level=alert_in.level,
        message=alert_in.message
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_alerts(db: Session, limit: int = 25):
    return db.query(models.AlertRecord).order_by(models.AlertRecord.created_at.desc()).limit(limit).all()


def create_analytics_snapshot(db: Session, analytics_in: schemas.AnalyticsSnapshotCreate) -> models.AnalyticsSnapshot:
    snapshot = models.AnalyticsSnapshot(
        session_id=analytics_in.session_id,
        metric=analytics_in.metric,
        value=analytics_in.value
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


def get_analytics(db: Session, limit: int = 25):
    return db.query(models.AnalyticsSnapshot).order_by(models.AnalyticsSnapshot.collected_at.desc()).limit(limit).all()


def create_report(db: Session, report_in: schemas.ReportCreate) -> models.ReportRecord:
    report = models.ReportRecord(
        name=report_in.name,
        type=report_in.type,
        file_path=report_in.file_path
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_reports(db: Session, limit: int = 25):
    return db.query(models.ReportRecord).order_by(models.ReportRecord.created_at.desc()).limit(limit).all()
