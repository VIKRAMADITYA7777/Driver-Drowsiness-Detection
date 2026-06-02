from pathlib import Path
from app.vision.pipeline import VisionPipeline
from app.vision.lstm_pipeline import LSTMPipeline


def main():
    source = Path("0")
    output = Path("backend/vision_output")
    output.mkdir(parents=True, exist_ok=True)

    pipeline = VisionPipeline(
        source=source,
        output=output
    )
    frames_processed = pipeline.run()
    print(f"Processed {frames_processed} frames with VisionPipeline.")

    lstm_pipeline = LSTMPipeline(
        source=source,
        output=output / "lstm",
        cnn_model_path=Path("models/cnn_drowsiness.h5"),
        lstm_model_path=Path("models/lstm_drowsiness.h5")
    )
    lstm_frames = lstm_pipeline.run()
    print(f"Processed {lstm_frames} frames with LSTMPipeline.")


if __name__ == '__main__':
    main()
