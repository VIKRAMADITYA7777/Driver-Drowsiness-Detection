from sqlalchemy.orm import Session
from app import models, schemas


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
