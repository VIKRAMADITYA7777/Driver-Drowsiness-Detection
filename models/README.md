# Models

Trained models and training scripts.

## Training

Use the CNN training script to build a drowsiness classification model from the processed dataset.

- Preprocess raw data with `datasets/pipeline.py`
- Save processed images into `datasets/pipeline_output/processed`
- Run training with:
  ```bash
  python models/train_cnn.py
  ```

The trained model is saved as `models/cnn_drowsiness.h5`.

## Inference

Use the inference script to run live predictions with the trained CNN model.

- `python models/infer_cnn.py` to open the default webcam
- `python models/infer_cnn.py <video_path>` to run inference on a video file

The inference code loads `models/cnn_drowsiness.h5` and overlays the predicted drowsiness class plus confidence.
