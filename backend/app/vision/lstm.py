from pathlib import Path
import numpy as np
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

IMAGE_SIZE = (224, 224)
SEQUENCE_LENGTH = 12
FEATURE_LAYER = "dense_1"


class LSTMSequenceModel:
    def __init__(self, cnn_model_path: Path, lstm_model_path: Path | None = None):
        self.feature_extractor = self._load_feature_extractor(cnn_model_path)
        self.lstm_model = load_model(str(lstm_model_path)) if lstm_model_path else None

    def _load_feature_extractor(self, model_path: Path) -> Model:
        model = load_model(str(model_path))
        if FEATURE_LAYER not in [layer.name for layer in model.layers]:
            raise ValueError(f"Feature layer '{FEATURE_LAYER}' not found in CNN model")
        return Model(inputs=model.input, outputs=model.get_layer(FEATURE_LAYER).output)

    def extract_feature(self, frame: np.ndarray) -> np.ndarray:
        img = keras_image.array_to_img(frame)
        img = img.resize(IMAGE_SIZE)
        tensor = keras_image.img_to_array(img).astype("float32") / 255.0
        tensor = np.expand_dims(tensor, axis=0)
        feature = self.feature_extractor.predict(tensor, verbose=0)
        return feature[0]

    def build_sequence(self, frames: list[np.ndarray]) -> np.ndarray:
        features = [self.extract_feature(frame) for frame in frames]
        return np.stack(features, axis=0)

    def predict_sequence(self, sequence: np.ndarray) -> tuple[str, float]:
        if self.lstm_model is None:
            raise RuntimeError("LSTM model not loaded")
        prediction = self.lstm_model.predict(np.expand_dims(sequence, axis=0), verbose=0)
        index = int(np.argmax(prediction, axis=1)[0])
        confidence = float(np.max(prediction))
        classes = ["open_eye", "closed_eye", "yawning"]
        label = classes[index] if index < len(classes) else "unknown"
        return label, confidence
