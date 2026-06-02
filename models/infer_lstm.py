import sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.vision.inference import CNNInference
from app.vision.lstm import LSTMSequenceModel

MODEL_PATH = ROOT / "cnn_drowsiness.h5"
LSTM_MODEL_PATH = ROOT / "lstm_drowsiness.h5"
SEQUENCE_LENGTH = 12
WINDOW_STEP = 3


def main(source: str = "0"):
    cnn_inference = CNNInference(MODEL_PATH)
    lstm_inference = LSTMSequenceModel(MODEL_PATH, LSTM_MODEL_PATH)

    capture = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {source}")

    print(f"Loaded LSTM model: {LSTM_MODEL_PATH}")
    frames = []

    while True:
        success, frame = capture.read()
        if not success:
            break

        frames.append(frame)
        if len(frames) >= SEQUENCE_LENGTH:
            sequence = np.stack(frames[-SEQUENCE_LENGTH:], axis=0)
            label, confidence = lstm_inference.predict_sequence(sequence)
            annotated = cnn_inference.annotate_frame(frame, label, confidence)
        else:
            annotated = frame.copy()
            cv2.putText(annotated, "Warming up sequence...", (16, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 180, 90), 2)

        cv2.imshow("LSTM Inference", annotated)
        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
