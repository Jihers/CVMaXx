from ultralytics import YOLO
from PIL import Image

MODEL_PATH = r"C:\Users\USER\OneDrive\Documents\CDCS230\Sem 5\CVMaXx\outputs\classify\train3\weights\best.pt"

model = YOLO(MODEL_PATH)

def analyze_xray(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    results = model.predict(image, verbose=False)

    probabilities = results[0].probs
    class_id = int(probabilities.top1)
    confidence = float(probabilities.top1conf)

    stage = model.names[class_id].replace("Stage", "CS")

    return {
        "stage": stage,
        "confidence": confidence * 100
    }