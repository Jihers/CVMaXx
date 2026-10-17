
from ultralytics import YOLO

model_path = "outputs/train/train_1202/weights/last.pt"

model = YOLO(model_path)

print("Model task:", model.task)
print("Model classes:", model.names)
