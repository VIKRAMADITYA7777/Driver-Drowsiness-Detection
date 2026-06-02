from datetime import datetime, timedelta
import json
from typing import Dict

from app.database import SessionLocal
from app import models, crud
from app import schemas


def compute_aggregates(window_minutes: int = 5) -> Dict[str, float]:
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        detections = db.query(models.DetectionEvent).filter(models.DetectionEvent.created_at >= cutoff).all()
        alerts = db.query(models.AlertRecord).filter(models.AlertRecord.created_at >= cutoff).all()

        total_detections = len(detections)
        total_alerts = len(alerts)

        perclos_values = []
        scores = []
        for d in detections:
            if d.score:
                scores.append(d.score)
            if d.metadata:
                try:
                    m = json.loads(d.metadata)
                    if isinstance(m, dict) and 'perclos' in m:
                        perclos_values.append(float(m.get('perclos', 0.0)))
                except Exception:
                    pass

        avg_score = float(sum(scores) / len(scores)) if scores else 0.0
        avg_perclos = float(sum(perclos_values) / len(perclos_values)) if perclos_values else 0.0

        return {
            'detections': total_detections,
            'alerts': total_alerts,
            'avg_score': avg_score,
            'avg_perclos': avg_perclos,
        }
    finally:
        db.close()


def snapshot_and_store(window_minutes: int = 5, session_id: int | None = None):
    aggregates = compute_aggregates(window_minutes)
    db = SessionLocal()
    try:
        # store key metrics
        crud.create_analytics_snapshot(db, schemas.AnalyticsSnapshotCreate(
            session_id=session_id,
            metric='detections_per_window',
            value=aggregates['detections']
        ))
        crud.create_analytics_snapshot(db, schemas.AnalyticsSnapshotCreate(
            session_id=session_id,
            metric='alerts_per_window',
            value=aggregates['alerts']
        ))
        crud.create_analytics_snapshot(db, schemas.AnalyticsSnapshotCreate(
            session_id=session_id,
            metric='avg_score',
            value=aggregates['avg_score']
        ))
        crud.create_analytics_snapshot(db, schemas.AnalyticsSnapshotCreate(
            session_id=session_id,
            metric='avg_perclos',
            value=aggregates['avg_perclos']
        ))
    finally:
        db.close()
