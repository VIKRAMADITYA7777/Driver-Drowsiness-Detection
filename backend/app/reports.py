from pathlib import Path
import csv
from datetime import datetime, timedelta
from typing import Optional
from app.database import SessionLocal
from app import crud, schemas
from app import models
from app.analytics import compute_aggregates


REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_csv_report(session_id: Optional[int] = None, window_minutes: int = 60) -> Path:
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=window_minutes)

    aggregates = compute_aggregates(window_minutes)

    filename = f"report_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    out_path = REPORTS_DIR / filename

    # Collect detections & alerts for the window
    db = SessionLocal()
    try:
        detections = db.query(models.DetectionEvent).filter(models.DetectionEvent.created_at >= cutoff).all()
        alerts = db.query(models.AlertRecord).filter(models.AlertRecord.created_at >= cutoff).all()

        with open(out_path, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(['metric', 'value'])
            writer.writerow(['detections', aggregates['detections']])
            writer.writerow(['alerts', aggregates['alerts']])
            writer.writerow(['avg_score', aggregates['avg_score']])
            writer.writerow(['avg_perclos', aggregates['avg_perclos']])
            writer.writerow([])
            writer.writerow(['detections_details'])
            writer.writerow(['id', 'session_id', 'event_type', 'score', 'created_at', 'metadata'])
            for d in detections:
                writer.writerow([d.id, d.session_id, d.event_type, d.score, d.created_at, d.metadata])
            writer.writerow([])
            writer.writerow(['alerts_details'])
            writer.writerow(['id', 'session_id', 'level', 'message', 'created_at'])
            for a in alerts:
                writer.writerow([a.id, a.session_id, a.level, a.message, a.created_at])

    finally:
        db.close()

    # register report in DB
    db = SessionLocal()
    try:
        report_in = schemas.ReportCreate(name=filename, type='csv', file_path=str(out_path))
        report = crud.create_report(db, report_in)
    finally:
        db.close()

    return out_path
