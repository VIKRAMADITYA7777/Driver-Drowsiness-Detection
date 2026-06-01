from dataclasses import dataclass
from typing import List, Optional
import cv2
import mediapipe as mp
from app.vision.metrics import eye_aspect_ratio, mouth_aspect_ratio, perclos


@dataclass
class FaceMetrics:
    face_detected: bool
    landmarks: Optional[List[List[float]]]
    left_eye_ratio: float
    right_eye_ratio: float
    mouth_ratio: float
    perclos_value: float
    blink_count: int
    yawn_count: int
    fatigue_label: str
    annotated_frame: Optional[any]


class FaceLandmarksDetector:
    LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
    MOUTH_IDX = [78, 95, 88, 178, 87, 14, 317, 402, 318]

    EYE_CLOSED_THRESHOLD = 0.22
    MOUTH_OPEN_THRESHOLD = 0.65

    def __init__(self, max_faces: int = 1):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.eye_history: List[float] = []
        self.blink_count = 0
        self.yawn_count = 0
        self.last_eye_closed = False
        self.last_mouth_open = False

    def detect(self, frame: any) -> FaceMetrics:
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return FaceMetrics(False, None, 0.0, 0.0, 0.0, 0.0, self.blink_count, self.yawn_count, 'No face', frame)

        face_landmarks = results.multi_face_landmarks[0]
        landmarks = self._normalize_landmarks(face_landmarks.landmark, frame.shape)
        left_eye = [landmarks[idx] for idx in self.LEFT_EYE_IDX]
        right_eye = [landmarks[idx] for idx in self.RIGHT_EYE_IDX]
        mouth = [landmarks[idx] for idx in self.MOUTH_IDX]

        left_ratio = eye_aspect_ratio(left_eye)
        right_ratio = eye_aspect_ratio(right_eye)
        mouth_ratio = mouth_aspect_ratio(mouth)
        average_eye = (left_ratio + right_ratio) / 2.0
        self.eye_history.append(average_eye)
        if len(self.eye_history) > 150:
            self.eye_history.pop(0)

        eye_closed = average_eye <= self.EYE_CLOSED_THRESHOLD
        mouth_open = mouth_ratio >= self.MOUTH_OPEN_THRESHOLD

        if eye_closed and not self.last_eye_closed:
            self.last_eye_closed = True
        if not eye_closed and self.last_eye_closed:
            self.blink_count += 1
            self.last_eye_closed = False

        if mouth_open and not self.last_mouth_open:
            self.last_mouth_open = True
        if not mouth_open and self.last_mouth_open:
            self.yawn_count += 1
            self.last_mouth_open = False

        perclos_value = perclos(self.eye_history[-30:])
        fatigue_label = self._classify_fatigue(average_eye, mouth_ratio, perclos_value)

        annotated = frame.copy()
        self._draw_landmarks(annotated, face_landmarks)
        self._draw_metrics(annotated, left_ratio, right_ratio, mouth_ratio, perclos_value)

        return FaceMetrics(True, landmarks, left_ratio, right_ratio, mouth_ratio, perclos_value, self.blink_count, self.yawn_count, fatigue_label, annotated)

    def _normalize_landmarks(self, landmarks: List[any], shape: tuple) -> List[List[float]]:
        height, width = shape[:2]
        return [[l.x * width, l.y * height] for l in landmarks]

    def _draw_landmarks(self, frame: any, face_landmarks: any) -> None:
        self.mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(24, 255, 171), thickness=1, circle_radius=1)
        )

    def _draw_metrics(self, frame: any, left_ratio: float, right_ratio: float, mouth_ratio: float, perclos_value: float) -> None:
        cv2.rectangle(frame, (12, 12), (400, 170), (6, 13, 28), -1)
        cv2.putText(frame, f"EAR L: {left_ratio:.2f}", (18, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)
        cv2.putText(frame, f"EAR R: {right_ratio:.2f}", (18, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)
        cv2.putText(frame, f"MAR: {mouth_ratio:.2f}", (18, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)
        cv2.putText(frame, f"PERCLOS: {perclos_value:.2f}", (18, 114), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)
        cv2.putText(frame, f"Blinks: {self.blink_count}", (18, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)
        cv2.putText(frame, f"Yawns: {self.yawn_count}", (18, 166), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (190, 255, 255), 2)

    def _classify_fatigue(self, eye_ratio: float, mouth_ratio: float, perclos_value: float) -> str:
        if perclos_value > 0.30 or mouth_ratio > 0.75 or eye_ratio < 0.18:
            return 'Drowsy'
        if perclos_value > 0.20 or mouth_ratio > 0.65 or eye_ratio < 0.22:
            return 'Warning'
        return 'Alert'
