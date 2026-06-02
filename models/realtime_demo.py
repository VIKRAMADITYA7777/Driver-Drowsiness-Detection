import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.vision.realtime import RealTimeDetector

MODEL_CNN = ROOT / "cnn_drowsiness.h5"
MODEL_LSTM = ROOT / "lstm_drowsiness.h5"


def main(source: str = "0"):
    detector = RealTimeDetector(source=source, cnn_model=str(MODEL_CNN), lstm_model=str(MODEL_LSTM))
    detector.run()


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else "0"
    main(src)
