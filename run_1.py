from ultralytics import YOLO

def train_yolov8():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # Use YOLOv8n (nano) for faster training

    # Train the model on the GPU
    model.train(
        data='CVMaxx.yaml',      # Path to your data.yaml file
        epochs=50,             # Number of training epochs
        batch=16,              # Batch size
        imgsz=640,             # Image size
        device=0,              # Use GPU 0 (set device to '0', '1', etc., or 'cpu' to use the CPU)
        project='runs/train',  # Directory to save training results
        name='train_1202'          # Experiment name
    )

if __name__ == '__main__':
    train_yolov8()
