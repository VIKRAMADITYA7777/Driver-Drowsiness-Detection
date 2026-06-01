# Dataset Pipeline

This folder contains the dataset preparation pipeline for the Driver Drowsiness Detection project.

## Structure

- `datasets/raw/` - place raw images in class subfolders: `open_eye`, `closed_eye`, `yawning`
- `datasets/pipeline.py` - preprocessing and augmentation pipeline
- `datasets/pipeline_output/` - generated processed and augmented dataset output
- `datasets/requirements.txt` - dataset pipeline dependencies

## Features

- Resizes images to `224x224`
- Applies CLAHE for contrast enhancement
- Performs augmentation: horizontal flip, rotation, brightness/contrast variation
- Generates metadata CSV with dataset details

## Usage

```powershell
cd C:\Users\VICKY\Downloads\DDD\datasets
python pipeline.py
```

## Recommended layout

```
datasets/
  raw/
    open_eye/
    closed_eye/
    yawning/
  pipeline_output/
```

Create class folders and put your dataset images there before running the pipeline.
