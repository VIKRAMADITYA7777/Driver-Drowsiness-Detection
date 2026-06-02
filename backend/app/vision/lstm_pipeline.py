from pathlib import Path
import cv2
from app.vision.inference import CNNInference
from app.vision.lstm import LSTMSequenceModel


class LSTMPipeline:
    def __init__(self, source: Path, output: Path, cnn_model_path: Path, lstm_model_path: Path, sequence_length: int = 12):
        self.source = source
        self.output = output
        self.sequence_length = sequence_length
        self.cnn_inference = CNNInference(cnn_model_path)
        self.lstm_inference = LSTMSequenceModel(cnn_model_path, lstm_model_path)
        self.output.mkdir(parents=True, exist_ok=True)

    def run(self):
        capture = cv2.VideoCapture(str(self.source))
        if not capture.isOpened():
            raise RuntimeError(f"Unable to open source: {self.source}")

        frame_buffer = []
        frame_index = 0

        while True:
            success, frame = capture.read()
            if not success:
                break

            frame_buffer.append(frame)
            label = "warming"
            confidence = 0.0

            if len(frame_buffer) >= self.sequence_length:
                sequence = frame_buffer[-self.sequence_length:]
                sequence_array = self.lstm_inference.build_sequence(sequence)
                label, confidence = self.lstm_inference.predict_sequence(sequence_array)

            annotated = self.cnn_inference.annotate_frame(frame, label, confidence)
            output_path = self.output / f"lstm_frame_{frame_index:05d}.png"
            cv2.imwrite(str(output_path), annotated)

            frame_index += 1

        capture.release()
        return frame_index
