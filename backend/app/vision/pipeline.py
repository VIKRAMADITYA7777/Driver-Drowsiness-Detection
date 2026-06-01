from pathlib import Path
import cv2
from app.vision.face_landmarks import FaceLandmarksDetector


class VisionPipeline:
    def __init__(self, source: Path, output: Path):
        self.source = source
        self.output = output
        self.detector = FaceLandmarksDetector()
        self.output.mkdir(parents=True, exist_ok=True)

    def run(self):
        capture = cv2.VideoCapture(str(self.source))
        if not capture.isOpened():
            raise RuntimeError(f"Unable to open source: {self.source}")

        frame_index = 0
        while True:
            success, frame = capture.read()
            if not success:
                break

            metrics = self.detector.detect(frame)
            output_path = self.output / f"frame_{frame_index:05d}.png"
            cv2.imwrite(str(output_path), metrics.annotated_frame)
            frame_index += 1

        capture.release()
        return frame_index
