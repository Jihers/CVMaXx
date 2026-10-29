
from pathlib import Path

import cv2
import joblib
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent.parent

CLASSIFY_MODEL_PATH = BASE_DIR / "models" / "cvmaxx_classifier.joblib"
SCALER_PATH = BASE_DIR / "models" / "cvmaxx_scaler.joblib"
DETECT_MODEL_PATH = (
    BASE_DIR / "models" /  "best.pt"
)


def load_detection_model(model_path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(str(model_path))


def load_joblib_model(model_path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


detect_model = load_detection_model(DETECT_MODEL_PATH)
classify_model = load_joblib_model(CLASSIFY_MODEL_PATH)
scaler = load_joblib_model(SCALER_PATH)


def extract_morphological_features(image):
    if image.mode != "RGB":
        image = image.convert("RGB")

    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)

    binary = cv2.adaptiveThreshold(
        equalized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    features = {
        "area": 0.0,
        "perimeter": 0.0,
        "aspect_ratio": 0.0,
        "circularity": 0.0,
        "convex_hull_area": 0.0,
        "solidity": 0.0,
        "eccentricity": 0.0
    }

    if not contours:
        return features

    contour = max(contours, key=cv2.contourArea)

    area = float(cv2.contourArea(contour))
    perimeter = float(cv2.arcLength(contour, True))

    x, y, w, h = cv2.boundingRect(contour)
    hull = cv2.convexHull(contour)
    hull_area = float(cv2.contourArea(hull))

    moments = cv2.moments(contour)
    denominator = moments["mu20"] + moments["mu02"]

    eccentricity = 0.0
    if denominator != 0:
        eccentricity = float(
            np.sqrt(
                (moments["mu20"] - moments["mu02"]) ** 2
                + 4 * moments["mu11"] ** 2
            ) / denominator
        )

    features.update({
        "area": area,
        "perimeter": perimeter,
        "aspect_ratio": w / h if h else 0.0,
        "circularity": (
            4 * np.pi * area / perimeter**2 if perimeter > 0 else 0.0
        ),
        "convex_hull_area": hull_area,
        "solidity": area / hull_area if hull_area > 0 else 0.0,
        "eccentricity": eccentricity
    })

    return features


def prepare_classifier_features(image, detection_result):
    if detection_result.boxes is None or len(detection_result.boxes) < 3:
        raise ValueError(
            "Fewer than 3 vertebrae were detected. "
            "Please upload a clearer X-ray image."
        )

    # Follow the ordering used in the existing metadata-generation code.
    boxes = detection_result.boxes.data.cpu().numpy()
    boxes = sorted(boxes, key=lambda box: box[0])[:3]

    roi_names = ["cv2", "cv3", "cv4"]
    features = {}

    for roi_name, box in zip(roi_names, boxes):
        x1, y1, x2, y2 = map(int, box[:4])

        x1 = max(0, min(x1, image.width))
        x2 = max(0, min(x2, image.width))
        y1 = max(0, min(y1, image.height))
        y2 = max(0, min(y2, image.height))

        if x2 <= x1 or y2 <= y1:
            raise ValueError("A detected vertebra has an invalid bounding box.")

        crop = image.crop((x1, y1, x2, y2))
        morphology = extract_morphological_features(crop)

        for name, value in morphology.items():
            features[f"{roi_name}_{name}"] = value

        area = morphology["area"]
        perimeter = morphology["perimeter"]
        hull_area = morphology["convex_hull_area"]

        features[f"{roi_name}_area_perimeter_ratio"] = (
            area / perimeter if perimeter > 0 else 0.0
        )
        features[f"{roi_name}_convex_hull_area_ratio"] = (
            hull_area / area if area > 0 else 0.0
        )

    # Match the feature engineering used in Code 1.
    features.pop("cv2_aspect_ratio", None)
    features.pop("cv2_circularity", None)

    for name in [
        "cv2_area",
        "cv2_perimeter",
        "cv2_area_perimeter_ratio"
    ]:
        features[f"log_{name}"] = np.log1p(features[name])

    feature_df = pd.DataFrame([features])

    
    # Use the same feature order as the trained classifier.
    expected_features = classify_model.booster_.feature_name()
    missing = set(expected_features) - set(feature_df.columns)

    if missing:
        raise ValueError(f"Missing classifier features: {missing}")

    feature_df = feature_df[expected_features]

    # Reuse the scaler fitted in Code 1.
    scaled_features = [
        "cv2_area",
        "cv2_perimeter",
        "cv2_area_perimeter_ratio"
    ]

    feature_df[scaled_features] = scaler.transform(
        feature_df[scaled_features]
    )

    return feature_df


def analyze_xray(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    detection_results = detect_model.predict(
        image,
        conf=0.25,
        verbose=False
    )

    detection_result = detection_results[0]

    feature_df = prepare_classifier_features(image, detection_result)

    prediction = classify_model.predict(feature_df)[0]

    if isinstance(prediction, (int, np.integer, float, np.floating)):
        stage = f"CS{int(prediction)}"
    else:
        stage_text = str(prediction).strip()
        stage = stage_text.replace("Stage", "CS")
        if stage.isdigit():
            stage = f"CS{stage}"

    confidence = None

    if hasattr(classify_model, "predict_proba"):
        probabilities = classify_model.predict_proba(feature_df)[0]
        confidence = float(np.max(probabilities)) * 100

    return {
        "stage": stage,
        "confidence": confidence,
        "detection_results": detection_results
    }