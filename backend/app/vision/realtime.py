from pathlib import Path
import time
import json
import cv2
from app.vision.face_landmarks import FaceLandmarksDetector
from app.vision.inference import CNNInference
from app.vision.lstm import LSTMSequenceModel
from app.database import SessionLocal
from app import crud, schemas


class RealTimeDetector:
    ALERT_COOLDOWN = 8.0  # seconds between alerts

    def __init__(self, source: str = "0", cnn_model: Path | None = None, lstm_model: Path | None = None):
        self.source = source
        self.detector = FaceLandmarksDetector()
        self.cnn = CNNInference(cnn_model) if cnn_model and Path(cnn_model).exists() else None
        self.lstm = LSTMSequenceModel(Path(cnn_model), Path(lstm_model)) if (lstm_model and Path(lstm_model).exists()) else None
        self.db = SessionLocal()
        self.session = crud.create_session(self.db, schemas.SessionCreate(user_id=None))
        self.last_alert_at = 0.0

    def _should_alert(self, label: str, confidence: float, perclos: float) -> tuple[bool, str]:
        if perclos > 0.30 or (label == "closed_eye" and confidence > 0.85) or (label == "yawning" and confidence > 0.7):
            return True, "Drowsy"
        if perclos > 0.20 or (label == "closed_eye" and confidence > 0.6):
            return True, "Warning"
        return False, "Alert"

    def run(self):
        cap = cv2.VideoCapture(int(self.source) if str(self.source).isdigit() else str(self.source))
        if not cap.isOpened():
            raise RuntimeError(f"Unable to open source: {self.source}")

        frame_buffer = []
        seq_len = 12

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                metrics = self.detector.detect(frame)
                label = "unknown"
                confidence = 0.0

                if self.cnn:
                    label, confidence = self.cnn.predict(frame)

                if self.lstm:
                    frame_buffer.append(frame)
                    if len(frame_buffer) > seq_len:
                        frame_buffer.pop(0)
                    if len(frame_buffer) == seq_len:
                        seq = self.lstm.build_sequence(frame_buffer)
                        try:
                            lbl, conf = self.lstm.predict_sequence(seq)
                            label, confidence = lbl, conf
                        except Exception:
                            pass

                should_alert, level = self._should_alert(label, confidence, metrics.perclos_value)

                now = time.time()
                if should_alert and (now - self.last_alert_at) > self.ALERT_COOLDOWN:
                    message = {
                        "label": label,
                        "confidence": confidence,
                        "perclos": metrics.perclos_value,
                        "blinks": metrics.blink_count,
                        "yawns": metrics.yawn_count
                    }

                    detection_in = schemas.DetectionCreate(
                        session_id=self.session.id,
                        event_type=level,
                        score=confidence,
                        metadata=json.dumps(message)
                    )
                    crud.create_detection(self.db, detection_in)

                    alert_in = schemas.AlertCreate(
                        session_id=self.session.id,
                        level=level,
                        message=f"Real-time alert: {level} ({label})"
                    )
                    crud.create_alert(self.db, alert_in)

                    self.last_alert_at = now

                annotated = frame.copy()
                cv2.putText(annotated, f"Status: {metrics.fatigue_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 80), 2)
                if self.cnn:
                    cv2.putText(annotated, f"CNN: {label} {confidence:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 80), 2)

                cv2.imshow("RealTime Detector", annotated)
                if cv2.waitKey(1) == 27:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.db.close()
