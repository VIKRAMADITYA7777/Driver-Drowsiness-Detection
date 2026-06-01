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
