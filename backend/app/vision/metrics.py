from typing import Sequence
import numpy as np


def euclidean_distance(point_a: Sequence[float], point_b: Sequence[float]) -> float:
    return float(np.linalg.norm(np.array(point_a) - np.array(point_b)))


def eye_aspect_ratio(eye_points: Sequence[Sequence[float]]) -> float:
    a = euclidean_distance(eye_points[1], eye_points[5])
    b = euclidean_distance(eye_points[2], eye_points[4])
    c = euclidean_distance(eye_points[0], eye_points[3])
    if c == 0:
        return 0.0
    return (a + b) / (2.0 * c)


def mouth_aspect_ratio(mouth_points: Sequence[Sequence[float]]) -> float:
    a = euclidean_distance(mouth_points[2], mouth_points[8])
    b = euclidean_distance(mouth_points[3], mouth_points[7])
    c = euclidean_distance(mouth_points[0], mouth_points[4])
    if c == 0:
        return 0.0
    return (a + b) / (2.0 * c)


def perclos(eye_ratios: Sequence[float], threshold: float = 0.24) -> float:
    if len(eye_ratios) == 0:
        return 0.0
    closed_frames = sum(1 for ratio in eye_ratios if ratio <= threshold)
    return closed_frames / len(eye_ratios)
