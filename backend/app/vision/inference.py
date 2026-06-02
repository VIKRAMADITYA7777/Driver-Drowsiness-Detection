from pathlib import Path
import numpy as np
import cv2
from tensorflow.keras.models import load_model

IMAGE_SIZE = (224, 224)
CLASS_NAMES = ["open_eye", "closed_eye", "yawning"]


class CNNInference:
    def __init__(self, model_path: Path):
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = load_model(str(model_path))

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        if frame.ndim == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        image = cv2.resize(frame, IMAGE_SIZE)
        image = image.astype("float32") / 255.0
        return np.expand_dims(image, axis=0)

    def predict(self, frame: np.ndarray) -> tuple[str, float]:
        tensor = self.preprocess(frame)
        predictions = self.model.predict(tensor)
        index = int(np.argmax(predictions, axis=1)[0])
        confidence = float(np.max(predictions))
        label = CLASS_NAMES[index] if index < len(CLASS_NAMES) else "unknown"
        return label, confidence

    def annotate_frame(self, frame: np.ndarray, label: str, confidence: float) -> np.ndarray:
        annotated = frame.copy()
        text = f"{label} ({confidence:.2f})"
        cv2.putText(annotated, text, (16, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 220, 90), 2)
        return annotated
