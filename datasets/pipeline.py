import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


class DatasetConfig:
    image_size: Tuple[int, int] = (224, 224)
    classes: List[str] = ["open_eye", "closed_eye", "yawning"]
    clahe_clip: float = 2.0
    clahe_grid_size: Tuple[int, int] = (8, 8)
    augmentation_count: int = 2


class DatasetPipeline:
    def __init__(self, source_dir: Path, target_dir: Path, config: DatasetConfig):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.config = config
        self.raw_dir = self.source_dir
        self.processed_dir = self.target_dir / "processed"
        self.augmented_dir = self.target_dir / "augmented"
        self.metadata_path = self.target_dir / "metadata.csv"
        self._prepare_directories()

    def _prepare_directories(self):
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.augmented_dir.mkdir(parents=True, exist_ok=True)
        for class_name in self.config.classes:
            (self.processed_dir / class_name).mkdir(parents=True, exist_ok=True)
            (self.augmented_dir / class_name).mkdir(parents=True, exist_ok=True)

    def build(self, augment: bool = True) -> pd.DataFrame:
        metadata = []
        for class_name in self.config.classes:
            class_source = self.raw_dir / class_name
            if not class_source.exists():
                continue
            class_target = self.processed_dir / class_name
            for source_path in sorted(class_source.glob("*.*")):
                image = self._load_image(source_path)
                if image is None:
                    continue

                processed = self._process_image(image)
                output_path = class_target / source_path.name
                cv2.imwrite(str(output_path), processed)
                metadata.append(self._metadata_entry(class_name, output_path, processed))

                if augment:
                    augmented_paths = self._augment_and_save(processed, class_name, source_path.stem)
                    for aug_path in augmented_paths:
                        metadata.append(self._metadata_entry(class_name, aug_path, processed, augmented=True))

        df = pd.DataFrame(metadata)
        df.to_csv(self.metadata_path, index=False)
        return df

    def _load_image(self, path: Path) -> np.ndarray | None:
        image = cv2.imread(str(path))
        if image is None:
            print(f"Warning: could not read {path}")
            return None
        return cv2.resize(image, self.config.image_size)

    def _process_image(self, image: np.ndarray) -> np.ndarray:
        image = self._apply_clahe(image)
        image = self._normalize(image)
        return image

    def _apply_clahe(self, image: np.ndarray) -> np.ndarray:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=self.config.clahe_clip, tileGridSize=self.config.clahe_grid_size)
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    def _normalize(self, image: np.ndarray) -> np.ndarray:
        normalized = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        return normalized.astype(np.uint8)

    def _augment_and_save(self, image: np.ndarray, class_name: str, stem: str) -> List[Path]:
        paths = []
        for idx in range(1, self.config.augmentation_count + 1):
            augmented = self._apply_augmentation(image, idx)
            output_path = self.augmented_dir / class_name / f"{stem}_aug{idx}.png"
            cv2.imwrite(str(output_path), augmented)
            paths.append(output_path)
        return paths

    def _apply_augmentation(self, image: np.ndarray, seed: int) -> np.ndarray:
        rng = np.random.RandomState(seed)
        augmented = image.copy()
        if rng.rand() > 0.5:
            augmented = cv2.flip(augmented, 1)
        angle = rng.uniform(-15, 15)
        augmented = self._rotate(augmented, angle)
        alpha = rng.uniform(0.85, 1.15)
        beta = rng.uniform(-15, 15)
        augmented = cv2.convertScaleAbs(augmented, alpha=alpha, beta=beta)
        return augmented

    def _rotate(self, image: np.ndarray, angle: float) -> np.ndarray:
        h, w = image.shape[:2]
        matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        return cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    def _metadata_entry(self, class_name: str, path: Path, image: np.ndarray, augmented: bool = False) -> dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "class": class_name,
            "path": str(path),
            "width": image.shape[1],
            "height": image.shape[0],
            "channels": image.shape[2] if image.ndim == 3 else 1,
            "augmented": augmented
        }


def run_demo():
    config = DatasetConfig()
    pipeline = DatasetPipeline(
        source_dir=Path("datasets/raw"),
        target_dir=Path("datasets/pipeline_output"),
        config=config
    )
    metadata = pipeline.build(augment=True)
    print(metadata.head())


if __name__ == "__main__":
    run_demo()
