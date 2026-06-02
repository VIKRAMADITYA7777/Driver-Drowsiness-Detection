import sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from tensorflow.keras.models import load_model
from app.explainability import gradcam_for_frame

MODEL_PATH = ROOT / "cnn_drowsiness.h5"


def preprocess_image(img: np.ndarray) -> np.ndarray:
    img = img.astype("float32") / 255.0
    return img


def main(source: str = "0"):
    model = load_model(str(MODEL_PATH))
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open source: {source}")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        overlay, pred_index, conf = gradcam_for_frame(model, frame, preprocess_image)
        cv2.putText(overlay, f"Class: {pred_index} {conf:.2f}", (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow("Grad-CAM", overlay)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else "0"
    main(src)
