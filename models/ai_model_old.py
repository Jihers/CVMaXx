from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import numpy as np
from models.concavity_analysis import estimate_concavity

BASE_DIR = Path(__file__).resolve().parent.parent

CLASSIFY_MODEL_PATH = BASE_DIR / "outputs" / "classify" / "train3" / "weights" / "best.pt"
DETECT_MODEL_PATH = BASE_DIR / "outputs" / "train" / "train_1202" / "weights" / "last.pt"


def load_model(model_path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(str(model_path))


classify_model = load_model(CLASSIFY_MODEL_PATH)
detect_model = load_model(DETECT_MODEL_PATH)



def analyze_detected_vertebrae(image, detection_result):
    results = []

    if detection_result.boxes is None:
        return results

    image_array = np.array(image.convert("RGB"))
    height, width = image_array.shape[:2]

    for box in detection_result.boxes:
        coordinates = box.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = coordinates

        # Keep crop coordinates within the image.
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        if x2 <= x1 or y2 <= y1:
            continue

        crop = image_array[y1:y2, x1:x2]
        measurement = estimate_concavity(crop)

        class_id = int(box.cls[0].item())
        class_name = detect_model.names[class_id]

        results.append({
            "vertebra": class_name,
            "bbox": [x1, y1, x2, y2],
            "depth_px": measurement["depth_px"],
            "classification": measurement["classification"]
        })

    return results


def analyze_xray(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    detection_results = detect_model.predict(image, verbose=False)
    classification_results = classify_model.predict(image, verbose=False)

    probabilities = classification_results[0].probs
    class_id = int(probabilities.top1)
    confidence = float(probabilities.top1conf)

    stage = classify_model.names[class_id].replace("Stage", "CS")

    concavity_results = []

    if detection_results:
        concavity_results = analyze_detected_vertebrae(
            image,
            detection_results[0]
        )

    return {
        "stage": stage,
        "confidence": confidence * 100,
        "detection_results": detection_results,
        "concavity_results": concavity_results
    }
