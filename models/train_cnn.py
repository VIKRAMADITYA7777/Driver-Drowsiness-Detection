from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "datasets" / "pipeline_output" / "processed"
MODEL_OUTPUT = Path(__file__).resolve().parent / "cnn_drowsiness.h5"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 12


def build_cnn(input_shape=(224, 224, 3), num_classes=3) -> tf.keras.Model:
    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.08),
            layers.RandomZoom(0.08),
        ],
        name="data_augmentation"
    )

    model = models.Sequential([
        layers.Input(shape=input_shape, name="input_image"),
        data_augmentation,
        layers.Rescaling(1.0 / 255.0, name="rescale"),

        layers.Conv2D(32, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(name="pool_1"),

        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(name="pool_2"),

        layers.Conv2D(128, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(name="pool_3"),

        layers.Dropout(0.35),
        layers.Flatten(name="flatten"),
        layers.Dense(128, activation="relu", name="dense_1"),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation="softmax", name="output"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def prepare_datasets(data_dir: Path, image_size=IMAGE_SIZE, batch_size=BATCH_SIZE):
    if not data_dir.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: {data_dir}. Run the dataset pipeline first."
        )

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        str(data_dir),
        labels="inferred",
        label_mode="int",
        image_size=image_size,
        batch_size=batch_size,
        validation_split=0.2,
        subset="training",
        seed=42,
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        str(data_dir),
        labels="inferred",
        label_mode="int",
        image_size=image_size,
        batch_size=batch_size,
        validation_split=0.2,
        subset="validation",
        seed=42,
    )

    class_names = train_ds.class_names
    train_ds = train_ds.cache().shuffle(1000).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)

    return train_ds, val_ds, class_names


def main():
    print("Starting CNN training for drowsiness detection...")
    print(f"Using dataset directory: {DATA_DIR}")

    train_ds, val_ds, class_names = prepare_datasets(DATA_DIR)
    print(f"Detected classes: {class_names}")

    model = build_cnn(input_shape=(*IMAGE_SIZE, 3), num_classes=len(class_names))
    model.summary()

    checkpoint = callbacks.ModelCheckpoint(
        filepath=str(MODEL_OUTPUT),
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1,
    )
    early_stop = callbacks.EarlyStopping(
        monitor="val_loss", patience=4, restore_best_weights=True, verbose=1
    )
    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=2, verbose=1
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[checkpoint, early_stop, reduce_lr],
    )

    print(f"Training finished. Best model saved to {MODEL_OUTPUT}")
    return history


if __name__ == "__main__":
    main()
