import numpy as np
import cv2
from typing import Tuple
from tensorflow.keras.models import Model
import tensorflow as tf


def find_last_conv_layer(model: Model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    raise ValueError("No Conv2D layer found in model")


def make_gradcam_heatmap(img_array: np.ndarray, model: Model, last_conv_layer_name: str, pred_index: int = None) -> np.ndarray:
    grad_model = Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = int(tf.argmax(predictions[0]))
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()


def overlay_heatmap(heatmap: np.ndarray, image: np.ndarray, alpha: float = 0.4) -> np.ndarray:
    heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(image, 1 - alpha, heatmap_color, alpha, 0)
    return overlay


def gradcam_for_frame(model: Model, frame: np.ndarray, preprocess_fn, last_conv_layer_name: str | None = None) -> Tuple[np.ndarray, int, float]:
    img = cv2.resize(frame, (224, 224))
    input_tensor = preprocess_fn(img)
    input_tensor = np.expand_dims(input_tensor, axis=0)

    preds = model.predict(input_tensor)
    pred_index = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))

    if last_conv_layer_name is None:
        last_conv_layer_name = find_last_conv_layer(model)

    heatmap = make_gradcam_heatmap(input_tensor, model, last_conv_layer_name, pred_index)
    overlay = overlay_heatmap(heatmap, cv2.resize(frame, (224, 224)))
    return overlay, pred_index, confidence
