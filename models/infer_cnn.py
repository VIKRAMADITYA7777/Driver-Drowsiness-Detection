import sys
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.vision.inference import CNNInference

MODEL_PATH = Path(__file__).resolve().parent / "cnn_drowsiness.h5"


def main(source: str = "0"):
    inference = CNNInference(MODEL_PATH)
    capture = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {source}")

    print(f"Loaded model: {MODEL_PATH}")
    print("Press ESC to exit.")

    while True:
        success, frame = capture.read()
        if not success:
            break

        label, confidence = inference.predict(frame)
        annotated = inference.annotate_frame(frame, label, confidence)
        cv2.imshow("CNN Inference", annotated)

        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
