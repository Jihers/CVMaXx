import os
import cv2
import numpy as np
import json
from PIL import Image
from ultralytics import YOLO
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_model(model_path):
    """Load the YOLOv8 model from a given path."""
    try:
        model = YOLO(model_path)
        logging.info("Model loaded successfully from %s", model_path)
        return model
    except Exception as e:
        logging.error("Error loading model: %s", e)
        raise


def extract_stage_from_filename(filename):
    """
    Extract the stage (e.g., S1, S2, S3) from the filename.
    Returns an integer if found, otherwise None.
    """
    base_name = os.path.basename(filename)
    parts = base_name.split('_')
    if parts and parts[0].startswith('S') and parts[0][1:].isdigit():
        return int(parts[0][1:])
    return None



def extract_morphological_features(image):
    """
    Extract morphological features from a PIL image.
    Uses histogram equalization and adaptive thresholding for robust segmentation.
    Returns a dictionary of features.
    """
    # Ensure the image is in RGB mode
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply histogram equalization to improve contrast
    equalized = cv2.equalizeHist(gray)
    
    # Use adaptive thresholding for robust segmentation
    binary = cv2.adaptiveThreshold(
        equalized,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    features = {}
    
    if contours:
        # Assume the largest contour is the object
        contour = max(contours, key=cv2.contourArea)
        features['area'] = cv2.contourArea(contour)
        features['perimeter'] = cv2.arcLength(contour, True)
        
        # Calculate the aspect ratio from the bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        features['aspect_ratio'] = w / h if h != 0 else 0
        
        area = features['area']
        perimeter = features['perimeter']
        features['circularity'] = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
        
        # Compute convex hull and solidity
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        features['convex_hull_area'] = hull_area
        features['solidity'] = area / hull_area if hull_area > 0 else 0
        
        # Calculate eccentricity using image moments
        moments = cv2.moments(contour)
        if (moments["mu20"] + moments["mu02"]) != 0:
            eccentricity = np.sqrt(
                (moments["mu20"] - moments["mu02"]) ** 2 + 4 * (moments["mu11"] ** 2)
            ) / (moments["mu20"] + moments["mu02"])
            features['eccentricity'] = eccentricity
    else:
        logging.warning("No contours found in image.")
    
    return features



def generate_metadata(model, image_path, detected_images_dir):
    """
    Generate metadata from an image using the YOLO model.
    Returns a dictionary with stage information and ROI details.
    """
    stage = extract_stage_from_filename(image_path)
    if stage is None:
        logging.warning("No stage found in filename %s. Defaulting stage to None.", image_path)

    try:
        results = model(image_path, conf=0.25, save=True)
    except Exception as e:
        logging.error("Error during model inference on %s: %s", image_path, e)
        return {"stage": stage, "rois": []}

    # Access the first result (YOLOv8 returns a list)
    result = results[0]

    if result.boxes is None or len(result.boxes.data) == 0:
        logging.info("No objects detected in %s.", image_path)
        return {"stage": stage, "rois": []}

    # Get the default save directory for detected images and move the file if needed
    default_save_dir = model.predictor.save_dir
    detected_image_filename = os.path.basename(image_path)
    detected_image_path = os.path.join(default_save_dir, detected_image_filename)

    if os.path.exists(detected_image_path):
        os.makedirs(detected_images_dir, exist_ok=True)
        custom_detected_image_path = os.path.join(detected_images_dir, detected_image_filename)
        os.replace(detected_image_path, custom_detected_image_path)

    # Process detections (limit to predefined ROIs)
    detections = result.boxes.data
    rois = ['cv2', 'cv3', 'cv4']  # Predefined ROI names
    detections = sorted(detections, key=lambda box: box[0])
    metadata_rois = []

    try:
        image = Image.open(image_path)
    except Exception as e:
        logging.error("Error opening image %s: %s", image_path, e)
        return {"stage": stage, "rois": []}

    for i, box in enumerate(detections):
        if i >= len(rois):  # Only process as many ROIs as defined
            break
        x1, y1, x2, y2, confidence, class_id = box.tolist()
        cropped = image.crop((int(x1), int(y1), int(x2), int(y2)))
        morphological_features = extract_morphological_features(cropped)

        metadata_rois.append({
            "roi": rois[i],
            "bounding_box": {"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)},
            "confidence": float(confidence),
            "class_id": int(class_id),
            "morphological_features": morphological_features
        })

    metadata = {"stage": stage, "rois": metadata_rois}
    return metadata


def save_metadata(metadata, output_path):
    """Save metadata to a JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        logging.info("Metadata saved to %s", output_path)
    except Exception as e:
        logging.error("Error saving metadata to %s: %s", output_path, e)


def process_images_in_directory(model, image_dir, output_dir, detected_images_dir):
    """Process all images in a directory to generate metadata."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(detected_images_dir, exist_ok=True)

    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)
        if os.path.isfile(image_path):
            logging.info("Processing image: %s", image_file)
            try:
                metadata = generate_metadata(model, image_path, detected_images_dir)
                output_path = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}_metadata.json")
                save_metadata(metadata, output_path)
            except Exception as e:
                logging.error("Error processing %s: %s", image_file, e)


if __name__ == '__main__':
    # Update these paths as needed:
    model_path = 'C:/Users/Administrator/Desktop/ultralytics/runs/train/train_1202/weights/best.pt'  # Path to your YOLOv8 weights
    image_dir = "C:/Users/Administrator/Desktop/ultralytics/CVMaXX_data/images/new_testing"  # Input images directory
    output_dir = "C:/Users/Administrator/Desktop/ultralytics/new_testing_1503"  # Directory to save metadata JSONs
    detected_images_dir = "C:/Users/Administrator/Desktop/ultralytics/new_testing_1503"  # Directory for detected images

    model = load_model(model_path)
    process_images_in_directory(model, image_dir, output_dir, detected_images_dir)
