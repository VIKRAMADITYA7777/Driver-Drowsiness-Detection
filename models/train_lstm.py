from pathlib import Path
import cv2
import numpy as np
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.models import load_model

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "datasets" / "pipeline_output" / "processed"
CNN_MODEL_PATH = ROOT / "cnn_drowsiness.h5"
LSTM_MODEL_OUTPUT = ROOT / "lstm_drowsiness.h5"
SEQUENCE_LENGTH = 12
BATCH_SIZE = 16
EPOCHS = 14


def load_class_sequences(data_dir: Path, sequence_length: int = SEQUENCE_LENGTH, max_sequences: int = 120):
    sequences = []
    labels = []
    class_names = sorted([d.name for d in data_dir.iterdir() if d.is_dir()])

    for class_index, class_name in enumerate(class_names):
        image_paths = sorted((data_dir / class_name).glob("*.png"))
        if len(image_paths) < sequence_length:
            continue
        step = max(1, len(image_paths) // max_sequences)
        for start in range(0, len(image_paths) - sequence_length + 1, step):
            window = image_paths[start:start + sequence_length]
            if len(window) < sequence_length:
                continue
            sequences.append((window, class_index))
            if len(sequences) >= max_sequences * len(class_names):
                break

    return sequences, class_names


def build_feature_extractor(model_path: Path):
    model = load_model(str(model_path))
    return models.Model(inputs=model.input, outputs=model.get_layer("dense_1").output)


def image_to_feature(path: Path, extractor):
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Unable to read image {path}")
    image = cv2.resize(image, (224, 224))
    tensor = image.astype("float32") / 255.0
    tensor = np.expand_dims(tensor, axis=0)
    feature = extractor.predict(tensor, verbose=0)
    return feature[0]


def build_dataset(sequences, extractor):
    X = []
    y = []
    for paths, label in sequences:
        features = [image_to_feature(path, extractor) for path in paths]
        X.append(np.stack(features, axis=0))
        y.append(label)
    return np.array(X), np.array(y)


def create_lstm_model(input_shape, num_classes):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.LSTM(72, return_sequences=False),
        layers.Dropout(0.35),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    print("Preparing LSTM training data...")
    sequences, class_names = load_class_sequences(DATA_DIR)
    if not sequences:
        raise RuntimeError("No sequence data found. Run the dataset pipeline first.")

    extractor = build_feature_extractor(CNN_MODEL_PATH)
    X, y = build_dataset(sequences, extractor)
    print(f"Loaded {len(X)} sequences for classes: {class_names}")

    sample_shape = X.shape[1:]
    model = create_lstm_model(sample_shape, len(class_names))
    model.summary()

    checkpoint = callbacks.ModelCheckpoint(
        filepath=str(LSTM_MODEL_OUTPUT),
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1,
    )
    early_stop = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1,
    )

    split = int(len(X) * 0.8)
    train_X, val_X = X[:split], X[split:]
    train_y, val_y = y[:split], y[split:]

    model.fit(
        train_X,
        train_y,
        validation_data=(val_X, val_y),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[checkpoint, early_stop],
    )

    print(f"LSTM training complete. Saved to {LSTM_MODEL_OUTPUT}")


if __name__ == "__main__":
    main()
