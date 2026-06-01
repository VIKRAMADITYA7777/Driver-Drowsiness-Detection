from pathlib import Path
from app.vision.pipeline import VisionPipeline


def main():
    pipeline = VisionPipeline(
        source=Path("0"),
        output=Path("backend/vision_output")
    )
    frames_processed = pipeline.run()
    print(f"Processed {frames_processed} frames.")


if __name__ == '__main__':
    main()
