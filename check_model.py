
from ultralytics import YOLO

model_path = r"C:\Users\USER\OneDrive\Documents\CDCS230\Sem 5\CVMaXx - Copy\outputs\train\train_1202\weights\last.pt"

model = YOLO(model_path)

print("Model task:", model.task)
print("Model classes:", model.names)
