
from pathlib import Path
from ultralytics import YOLO
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent

CLASSIFY_MODEL_PATH = BASE_DIR / "outputs" / "classify" / "train3" / "weights" / "best.pt"
DETECT_MODEL_PATH = BASE_DIR / "outputs" / "train" / "train_1202" / "weights" / "last.pt"


def load_model(model_path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(str(model_path))


classify_model = load_model(CLASSIFY_MODEL_PATH)
detect_model = load_model(DETECT_MODEL_PATH)


def analyze_xray(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    detection_results = detect_model.predict(image, verbose=False)
    classification_results = classify_model.predict(image, verbose=False)

    probabilities = classification_results[0].probs
    class_id = int(probabilities.top1)
    confidence = float(probabilities.top1conf)

    stage = classify_model.names[class_id].replace("Stage", "CS")

    return {
        "stage": stage,
        "confidence": confidence * 100,
        "detection_results": detection_results
    }
